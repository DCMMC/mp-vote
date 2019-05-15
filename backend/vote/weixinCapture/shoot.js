const phantom = require('phantom');

// 'https://mp.weixin.qq.com/s?__biz=MjM5NTgzMTY0Nw==&mid=2648928561&idx=1&sn=49bf482d9f7c4fbbfde63f9f07d06eca&chksm=bee55b018992d217a67a99014a2a2846424a25af7ff930081eb573f0f25f1f4629f6851366f7&mpshare=1&scene=1&srcid=0502ByFtDGZbHbUl9UXdKjzs#rd'
// console.log(process.argv)
const url_target = process.argv[2]
const tag_name = process.argv[3]

async function main(url) {
  const instance = await phantom.create();
  const page = await instance.createPage();

	console.log('debug')
  // await page.property('viewportSize', { width: 750, height: 1334 });
  await page.property('viewportSize', { width: 414, height: 736 });
  const status = await page.open(url);
  console.log(`Page opened with status [${status}].`);
	// Wait a bit for javascript to load and run
	await new Promise(resolve => setTimeout(resolve, 3000))
	console.log('sleep end')
	// await page.includeJs("https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js");
	// await page.includeJs("http://cdn.bootcss.com/jquery/2.1.4/jquery.mi.js").then(async (res) => {
		console.log('included js')
		await page.evaluate(function () {
			console.log('start image lazy loading');
			var $imgs = $('img');
			var size = 0;
			$imgs.each(function () {
					var src = $(this).attr("src");
					var data_src = $(this).attr("data-src")
					if (data_src) {
							$(this).attr("src", $(this).attr("data-src"));
							size++;
					}
			});
			return size;
		}).then((html) => {
			setTimeout(() => {
				page.render(__dirname + '/../media/' + tag_name + '.pdf');
				// console.log(`File created at [./demo.pdf]`);
				instance.exit();
			}, 3000);
		});
	// });
}

main(url_target);

