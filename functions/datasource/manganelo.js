const functions = require('firebase-functions');
const fetch = require('isomorphic-fetch');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const sourceName = "Manganelo";
const searchLink = "https://manganato.com/search/story/"
const chapterItemSelector = "body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-chapter-list > ul > li"
const descriptionSelector = "#panel-story-info-description";
const statusSelector = "body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-info > div.story-info-right > table > tbody > tr:nth-child(3) > td.table-value"
const ratingSelector = "#rate_row_cmd > em > em:nth-child(2) > em > em:nth-child(1)"

exports.search = async(searctTerm) => {
    try {
        functions.logger.info({ source: sourceName, function: "search", param: searctTerm });
        // Main function body
        const response = await fetch(`${searchLink}${searctTerm.toLowerCase().replace(/\W/i, '_')}`);
        const text = await response.text();
        const dom = new JSDOM(text);
        var result = [];
        dom.window.document.querySelectorAll("div.search-story-item").forEach(_parseItem);

        function _parseItem(value, index, array) {
            const _dom = new JSDOM(value.innerHTML);
            var name = _dom.window.document.querySelector("div h3 a").textContent;
            var link = _dom.window.document.querySelector("div h3 a").getAttribute('href');
            var coverPicture = _dom.window.document.querySelector("a.item-img img").getAttribute('src');

            result.push({
                "name": name,
                "link": link,
                "type": "manga",
                "imageType": "online",
                "coverPicture": coverPicture,
                "lastRead": "",
                "lastChapterRead": ""
            })
        }
        // End Main function body
        return result;
    } catch (e) {
        functions.logger.error({ source: sourceName, function: "search", error: e.message });
        throw e;
    }
};

exports.details = async(mangaLink) => {
    try {
        functions.logger.info({ source: sourceName, function: "details", param: mangaLink });
        // Main function body
        const response = await fetch(mangaLink);
        const text = await response.text();
        const dom = new JSDOM(text);
        var result = {
            "status": "",
            "rating": 0,
            "description": "",
            "chapter_count": 0,
            "chapters": [],
        };
        dom.window.document.querySelectorAll(chapterItemSelector).forEach(_getChapters);
        result.description = dom.window.document.querySelector(descriptionSelector).textContent.replace('\nDescription :\n', "")
        result.status = dom.window.document.querySelector(ratingSelector).textContent

        function _getChapters(value, index, array) {
            var chapter = {
                "index": index,
                "name": "",
                "link": ""
            };
            const _dom = new JSDOM(value.innerHTML);
            chapter.name = _dom.window.document.querySelector("a").textContent;
            chapter.link = _dom.window.document.querySelector("a").getAttribute('href');

            result.chapters.push(chapter);
            result.chapter_count++;
        }
        // End Main function body
        return result;
    } catch (e) {
        functions.logger.error({ source: sourceName, function: "search", error: e.message });
        throw e;
    }
}