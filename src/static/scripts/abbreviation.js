const abbrs = {
  "მრ. არსებ. სახ.": "მრავლობითი არსებითი სახელი - plural noun",
  "არსებ. სახ.": "არსებითი სახელი - noun",
  "ზედს. სახ.": "ზედსართავი სახელი - adjective",
  "ზმნ.": "ზმნა - verb",
  "აბრევ.": "აბრევიატურა - abbreviation",
  "აგრ.": "აგრეთვე - also",
  "ამერ.": "ამერიკული ინგლისური - American English",
  "ა.შ.": "(და) ასე შემდეგ - (and) so on",
  "განსაკ.": "განსაკუთრებით - especially",
  "იშვ.": "იშვიათი - rare",
  "იხ.": "იხილე - see",
  "მაგ.": "მაგალითად - for example",
  "მოძვ.": "მოძველებული - obsolete",
  "საუბ.": "სასაუბრო, საუბრული - colloquial, informal",
  "სლ.": "სლენგი - slang",
  "უპირატ.": "უპირატესად - chiefly",
  "შდრ.": "შეადარე - compare",
  "შემოკლ.": "შემოკლებული ფორმა - short form",
  "ჩვეულ.": "ჩვეულებრივ - usually",
  "ხშ.": "ხშირად - often"
};

const elementsWithAbbrs = document.querySelectorAll(".abbr-support");

function unabbreviate(el) {
  for(const abbr in abbrs){
    el.innerHTML = el.innerHTML.replaceAll(abbr, `<abbr class="abbreviation" title="${abbrs[abbr]}">${abbr}</abbr>`)
  }
}

for (const el of elementsWithAbbrs) {
  unabbreviate(el);
}
