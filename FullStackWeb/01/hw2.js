var color = ['red','yellow','blue','red','purple','pink'];

function do_game(){
    var target_index,target,guess_input;
    var count = 0;
    target_index = Math.floor(Math.random()*(color.length-1));
    target = color[target_index];
    console.log(target);
    while(1){
        guess_input = window.prompt("I am thinking of one of these colors:\n"+color.sort().join()+"\nWhat color am I thinkg of?") ;
        count += 1;
        if(check_guess(target,guess_input)){
            var myBody=document.getElementsByTagName("body")[0];
            myBody.style.background=target;
            break;}
    } 
}

function check_guess(target,guess){
    if(color.indexOf(guess)==-1){alert("out of range");return 0;}
    if(guess > target){alert("guess>target");return 0;}
    if(guess < target){alert("guess<target");return 0;}
    if(guess = target){alert("guess=target");return 1;}
    return 0;
}
