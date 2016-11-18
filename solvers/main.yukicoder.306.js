var lines = [];
var counter = 0;
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});
reader.on('line', function (line) {
  counter += 1;
  lines.push(line);
  if( counter == 2 ) { 
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
    x.split(" ").map(function(x2){
      ents.push(parseFloat(x2));
    });
  });
  var ax = ents[0];
  var ay = ents[1];
  var bx = ents[2];
  var by = ents[3];
  var k  = (by - ay)/( bx + ax );
  console.log(ay + k * ax);
}
