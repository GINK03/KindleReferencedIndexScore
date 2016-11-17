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
    x.split(" ").map(function(x2) {
      ents.push(x2);
    });
  });
  var aite = ents[1];
  var jibun = ents[0];
  if ( aite == jibun ) { console.log("Drew"); };
  if ( aite == 0 && jibun == 1 ) { console.log("Lost"); };
  if ( aite == 1 && jibun == 2 ) { console.log("Lost"); };
  if ( aite == 2 && jibun == 0 ) { console.log("Lost"); };
  if ( aite == 0 && jibun == 2 ) { console.log("Win"); };
  if ( aite == 1 && jibun == 0 ) { console.log("Win"); };
  if ( aite == 2 && jibun == 1 ) { console.log("Win"); };
}
