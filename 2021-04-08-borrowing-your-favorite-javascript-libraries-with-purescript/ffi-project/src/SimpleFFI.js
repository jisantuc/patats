exports.leftPadImpl = function(s, padLength, leader) {
    return s.padStart(padLength, leader);
}

exports.foo = function(s) { 
    return () => console.log(s);
}