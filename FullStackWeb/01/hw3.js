var numberOfFaces=5;

function generateFaces(){
    var theLeftSide=document.getElementById("leftside");
    for(var i=0;i<numberOfFaces;i++){
        var img=document.createElement("img");
        //img.setAttribute("src","smile.png");
        img.src="smile.png"
        //firefox
        //img.style.left=Math.floor(Math.random()*400);
        //img.style.top=Math.floor(Math.random()*400);
        //IE
        img.setAttribute("style","left:"+Math.floor(Math.random()*400)+"px;top:"+Math.floor(Math.random()*400)+"px")
        theLeftSide.appendChild(img);
    }

    var theRightSide=document.getElementById("rightside");
    var leftSideImages=theLeftSide.cloneNode(true);
    leftSideImages.removeChild(leftSideImages.lastChild);
    theRightSide.appendChild(leftSideImages);
    
    theLeftSide.lastChild.onclick=function nextLevel(event){
        event.stopPropagation();
        numberOfFaces +=5;
        while(theLeftSide.firstChild!=null){
            theLeftSide.removeChild(theLeftSide.firstChild);
            }
        theRightSide.removeChild(theRightSide.firstChild)
        generateFaces();
        }; 

    var theBody=document.getElementsByTagName("body")[0];
    theBody.onclick=function gameOver(){
        alert("Game Over!");
        theBody.onclick=null;
        theLeftSide.lastChild.onclick=null;
        };
}
