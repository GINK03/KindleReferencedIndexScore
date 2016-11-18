var lines = [];
var counter = 0;
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});
reader.on('line', function (line) {
  counter += 1;
  lines.push(line);
  if( counter == 1 ) { 
    main();
    process.exit(0);
  }
});
process.stdin.on('end', function () {
  //do something
});

function main(){
  ents = [];
  lines.map(function(x){
    var num = parseInt(x);
    if ( num == 0 ) {
      console.log(1);
    } else {
      console.log(0);
    }
  });
}
