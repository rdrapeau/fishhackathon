var Scraper = require ('images-scraper')
  , bing = new Scraper.Bing();

bing.list({
	keyword: 'caught bass',
	num: 1000,
	detail: true
})
.then(function (res) {
	console.log(res.map(function(x) { return x.url; }).join('\n'));
}).catch(function(err) {
	console.log('err',err);
})
