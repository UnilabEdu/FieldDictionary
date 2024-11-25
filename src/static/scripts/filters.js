const filterContent = document.querySelector(".filter-content");

const checkboxGroups = document.querySelectorAll(".checkbox-group");

const searchLetterInput = filterContent.querySelector("#checkbox-search-field");

searchLetterInput.addEventListener("keyup", searchFilters);

checkboxGroups.forEach((checkboxGroup) => {
  makeFilterToggleable(checkboxGroup); // Make filter subfields togglable
  makeFiltersDerived(checkboxGroup); // Make connect field and subfield state
});

// tag derevations are coming from the backend right now, uncommenting would turn on client site derevations,
// but there is a mismatch of behaviours between them.
// makeTagsDerived();
makeFiltersResetable();
searchFilters();

function makeFiltersResetable() {
  const resetFiltersButton = filterContent.querySelector(
    ".reset-filters-button",
  );

  resetFiltersButton?.addEventListener("click", () => {
    const checkboxes = filterContent.querySelectorAll("input[type=checkbox]");

    checkboxes.forEach((checkbox) => {
      checkbox.checked = 0;
      checkbox.dispatchEvent(new Event("update"));
    });
  });
}

function makeFilterToggleable(checkboxGroup) {
  const arrowBtn = checkboxGroup.querySelector(
    ".checkbox-container > .vector-button",
  );

  if (!arrowBtn) return;

  const checkboxList = checkboxGroup.querySelector(".checkbox-list");

  if (!checkboxList) {
    arrowBtn.disabled = true;
    return;
  }

  arrowBtn.addEventListener("click", () => {
    checkboxGroup.classList.toggle("open");
  });
}

function makeFiltersDerived(checkboxGroup) {
  const filterCheckbox = checkboxGroup.querySelector(
    ".checkbox-container > input",
  );

  const subfilterCheckboxes = checkboxGroup.querySelectorAll(
    "& > .checkbox-list input",
  );

  function checkIfAllSubsChecked() {
    const isEverySubfilterChecked = [...subfilterCheckboxes]
      .map((x) => x.checked)
      .every((x) => x);

    if (isEverySubfilterChecked) {
      filterCheckbox.checked = true;
    } else {
      filterCheckbox.checked = false;
    }
  }

  subfilterCheckboxes.forEach((subfilterCheckbox) => {
    subfilterCheckbox.addEventListener("change", () => {
      checkIfAllSubsChecked();
      filterCheckbox.dispatchEvent(new Event("update"));
    });

    subfilterCheckbox.addEventListener("update", () => {
      checkIfAllSubsChecked();
      filterCheckbox.dispatchEvent(new Event("update"));
    });
  });

  filterCheckbox.addEventListener(
    "change",
    (e) => {
      subfilterCheckboxes.forEach(
        (checkbox) => (checkbox.checked = e.target.checked),
      );

      filterCheckbox.dispatchEvent(new Event("update"));
    },
    { capture: true },
  );
}

function makeTagsDerived() {
  const filterCheckboxes = filterContent.querySelectorAll(
    'input[type="checkbox"]',
  );

  filterCheckboxes.forEach((el) =>
    el.addEventListener("update", setFilterLabels),
  );
}

function setFilterLabels() {
  const filterLabelSlot = document.querySelector("#filter-label-slot");
  const topLevelFilterData = getTopLevelFilterData();

  filterLabelSlot.innerHTML = topLevelFilterData
    .sort((a, b) => a.label.localeCompare(b.label)) // Sorting alphabetically
    .map(
      (filterData) => `
              <li class="selected-filter-item">
                ${filterData.label}
                <button id="${filterData.checkboxId}-remove-button" class="selected-filter-remove-button vector-button">
                  <img src="/static/images/x.svg" />
                </button>
              </li>`,
    )
    .join("");

  // Make it so clicking the remove button unchecks the checkbox
  topLevelFilterData.forEach((filterData) => {
    const removeButton = document.querySelector(
      `#${filterData.checkboxId + "-remove-button"}`,
    );
    const checkbox = document.querySelector(`#${filterData.checkboxId}`);

    removeButton.addEventListener("click", () => {
      checkbox.checked = false;
      checkbox.dispatchEvent(new Event("change"));
    });
  });

  filterLabelSlot.style.display =
    topLevelFilterData.length > 0 ? "flex" : "none";
}

function getTopLevelFilterData() {
  const rootCheckboxGroups = filterContent.querySelectorAll(
    ".checkbox-list.level-1 > .checkbox-group",
  );

  const checkboxData = [];
  let queue = [...rootCheckboxGroups];
  let maxIter = 1 << 16;

  while (queue.length > 0 && maxIter-- > 0) {
    const currCheckboxGroup = queue.shift();
    const currCheckboxData = getCheckboxData(currCheckboxGroup);

    if (currCheckboxData.checked) {
      checkboxData.push(currCheckboxData);
    } else {
      const childCheckboxes = currCheckboxGroup.querySelectorAll(
        "& > .checkbox-list > .checkbox-group",
      );

      queue = [...queue, ...childCheckboxes];
    }
  }

  return checkboxData;
}

function getCheckboxData(checkboxGroup) {
  const checkbox = checkboxGroup.querySelector(
    '& > .checkbox-container input[type="checkbox"]',
  );
  const label = checkboxGroup.querySelector("& >.checkbox-container label");

  return {
    checkboxId: checkbox.id,
    checked: checkbox.checked,
    label: label.textContent,
  };
}

function searchFilters() {
  const rootCheckboxGroups = filterContent.querySelectorAll(
    ".checkbox-list.level-1 > .checkbox-group",
  );

  const query = searchLetterInput.value;

  matchChildren(query, rootCheckboxGroups);
}

function recMatchFilter(query, rootEl) {
  const label = rootEl.querySelector(
    "& > .checkbox-container label",
  ).textContent;

  const children = rootEl.querySelectorAll(
    "& > .checkbox-list .checkbox-group",
  );

  const checkboxButton = rootEl.querySelector(
    "& > .checkbox-container .toggle-button",
  );

  const hasMatchingChildren = matchChildren(query, children);
  const didMatch = hasMatchingChildren | matchString(query, label);

  if (didMatch) {
    rootEl.style.display = "block";
  } else {
    rootEl.style.display = "none";
  }

  if (checkboxButton) {
    // if children dont match the query hide them,
    // if they do show them and open the sublist
    if (hasMatchingChildren) {
      checkboxButton.style.display = "block";
      if (!rootEl.classList.contains("open")) {
        checkboxButton.click();
      }
    } else {
      checkboxButton.style.display = "none";
    }


    // to close all sublists when empty query is given
    if (query.length === 0) {
      if (rootEl.classList.contains("open")) {
        checkboxButton.click();
      }
    }
  }

  return didMatch;
}

function matchChildren(query, elements) {
  if (elements.length === 0) return false;
  let didMatchAny = false;

  elements.forEach((el) => {
    didMatchAny |= recMatchFilter(query, el);
  });

  return didMatchAny;
}

// using very basic match algo for now
function matchString(qeury, str) {
  return str.startsWith(qeury);
}
