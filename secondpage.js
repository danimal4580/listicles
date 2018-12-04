//
const reader = new FileReader()

function read(input) {
	const csv = input.files[0]
	reader.readAsText(csv)
}

reader.onload = function (e) {
	result = e.target.result
	table = []
	rows = result.split('\n')
	// hardcoded the one
	for (i = 1; i < rows.length; i++) {
		columns = rows[i].split('%')
		columns[columns.length-1] = columns[columns.length-1].replace('[', '');
		columns[columns.length-1] = columns[columns.length-1].replace(']', '');
    	table.push(columns)
	}

	for (i = 0; i<2; i++) {


		// Set Columns
		var j = 0
		var colCounter = 0
		while (colCounter < 2) {

			col = table[i][j]

			if (col != '') {
				console.log(col)
				document.getElementById("row"+i.toString()+"col"+colCounter.toString()).innerHTML = col
				colCounter = colCounter + 1
			}

			j = j +1
		}
		// Set Photo
		var last = table[i].pop()
		last = last.trim()
		console.log(last)
		document.getElementById("row"+i.toString()+"img").src = last

	}
}

console.log('exitingdansjs');



	// console.log(table[0][table[0].length])
	// document.getElementById("img1").src = table[0][table[0].length]
	// console.log(document.getElementById("img1").src)
	// console.log(e.target.result)
	// location.reload();

// parsedResults = null

// const fs = require('browserify-fs');
// const papa = require('papaparse');
// console.log('adsf');
// console.log(process.cwd());
// console.log(fs.existsSync('temp.txt'))
// const file = fs.createReadStream('temp.txt');
// // const file = fs.readFile('what.csv', function (err, data) {
// //     if (err) return console.error(err);
// //    console.log(data.toString());
// // });
// // console.log(file)
// papa.parse(file, {
// 	error: function(err, file) {
//             console.log(err);
//             console.log(file)
//      },
// 	complete: function(results) {
// 		console.log('inside')
// 		console.log(results)
// 		console.log("Finished:", results.data);
// 	}
// });
// console.log('hiya')

// // require(['fs'], function (fs) {
// // 	require(['papaparse'], function(papa) {
// // 		const file = fs.createReadStream('demo1.csv');
// // 		papa.parse(file, {
// // 			complete: function(results) {
// // 			parsedResults = results
// // 			console.log("Finished:", results.data);
// // 			}
// // 		})
// // 	});
// // });
// // console.log('neat')
// // console.log(parsedResults)


// // let parsedResults = null
