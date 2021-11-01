const functions = require('firebase-functions');
const fetch = require('isomorphic-fetch');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

var sourceName = "Manganelo";
var searchLink = "https://manganato.com/search/story/"

exports.search = async(searctTerm) => {
    try {
        functions.logger.info({ source: sourceName, function: "search", param: searctTerm });
        // Main function body
        const response = await fetch(`${searchLink}${searctTerm.toLowerCase().replace(/\W/i, '_')}`);
        const text = await response.text();
        const dom = new JSDOM(text);
        var result = [];
        var items = dom.window.document.querySelectorAll("div.search-story-item").forEach(_parseItem);

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