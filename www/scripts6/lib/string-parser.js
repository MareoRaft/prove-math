function string_parser(string_test){
//var string_test='Here is a test <img1> and here is a question A tree <<[is]|is not>> an object and the answer is [[10]].Here is <<[exists]| does not exist>> another picture <img2>. Check this one out too [[true]]'


//var string_test1='There is nothing to replace here'



var path='<img src="path/to/the/image/'
var content='<span class="coverup">'
var options='<span class="options">'

if(string_test.match(/<img[0-9]+>/)){
 var res1=string_test.match(/<img[0-9]+>/g)
 for (var i=0;i<res1.length;i++){
 x=res1[i].replace('<','').replace('>','')
 im_file1=path.concat(x,'.jpg">')
 string_test=string_test.replace(res1[i],im_file1)
 }
}


if(string_test.match(/\[\[.*\]\]/)){
 var res2 = string_test.match(/\[\[((?!\]\]).)*\]\]/gi)
 for(var i=0;i<res2.length;i++){
 y=res2[i].replace('[[','').replace(']]','')
 string_test=string_test.replace(res2[i],content.concat(y,'</span>'))
 }
}


if(string_test.match(/<<.*>>/g)){
 var res3 = string_test.match((/<<((?!>>).)*>>/gi))
 for (var i=0;i<res3.length;i++){
 var choice=res3[i].replace('<<','').replace('>>','').split("|")
 z=options
  for (var j=0;j<choice.length;j++){
   if(choice[j].startsWith('[')){
      alert(choice[j])
      z=z.concat('<span class="correct">',choice[j].replace('[','').replace(']',''),'</span>')

   }
   else{
      z=z.concat('<span>',choice[j],'</span>')
   }

  }
 z=z.concat('</span>')
 string_test=string_test.replace(res3[i],z)
 }
}


}
