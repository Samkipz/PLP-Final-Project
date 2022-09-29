
//===========================USER FEEDBACK MORESO STAR RATINGS ============================//

//get all stars by id as one, two, three, four and five
const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');

//get the user add feedback form ('rate-form') and the csrf middleware token
const form = document.querySelector('.rate-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

/*---------------------------------------------------------------------------------------------
    The function handleStarSelect(size) below,  checks if a user has selected a star, it should 
    also select all other stars behind it i.e all stars less than parameter (size). That is, 
    if a user selects the third star, star one, two and three should also be selected automatically
    -form.children[2].children will select all the five stars to a variable children then we loop
    through adding class 'checked' or removing class 'checked' for 'false condition'
-----------------------------------------------------------------------------------------------*/
const handleStarSelect = (size) => {
    const children = form.children[2].children
    for(let i=0; i<children.length; i++){
        if(i <= size) {
            children[i].classList.add('checked')
        }
        else{
            children[i].classList.remove('checked')
        }
    }
}

/*  ---------------------------------------------------------------
Now, how do we get the size variable above? We use Switch case, 
then for every case, if true, we call the handleStarSelect function
------------------------------------------------------------------*/

const handleSelect = (selection) => {
    switch(selection){
        case 'first':{
            handleStarSelect(0)
            return
        }
        case 'second':{
            handleStarSelect(1)
            return
        }
        case 'third':{
            handleStarSelect(2)
            return
        }
        case 'fourth':{
            handleStarSelect(3)
            return
        }
        case 'fifth':{
            handleStarSelect(4)
            return
        }
    }
}

/*----------------------------------------------------------------------
Once we obtain total number of selected star, we need to pass it to the 
server as numeric value. The getNumericValue function below gets the id of 
the 'clicked' star passed to it as string value then returns a numeric value
--------------------------------------------------------------------------*/
const getNumericValue = (stringValue) => {
    let numericValue;

    if(stringValue === 'first'){
        numericValue = 1
    }else if( stringValue === 'second'){
        numericValue = 2
    }else if( stringValue === 'third'){
        numericValue = 3
    }else if( stringValue === 'fourth'){
        numericValue = 4
    }else if( stringValue === 'fifth'){
        numericValue = 5
    }else{
        numericValue =0
    }
    return numericValue
}

/* -------------------------------------------------------------------------------
If a star exist, check for mouse over event and call the handleSelect
function on it (which gets size and calls on handleStarSelect to perform styling)
----------------------------------------------------------------------------------*/
if (one) {
    const arr = [one, two, three, four, five]
    arr.forEach(item => item.addEventListener('mouseover', (event) =>{
        handleSelect(event.target.id)
    }))

    //If user clicks on a star, get the star id and, call on getNumericValue function
    //store the returned numeric value to a variable called val_num
    let val;
    arr.forEach(item => item.addEventListener('click', (event) =>{
        val = event.target.id
    }))
    form.addEventListener('submit', e=>{
        e.preventDefault()
        const my_url = "add_feedback"   //---------------------------> url to handle post request
        const id = e.target.id          //---------------------------> Rental id (passed to server through ajax)
        const msg = document.getElementById('msg').value //----------> User message (passed to server through ajax)
        const val_num = getNumericValue(val) //----------------------> Value/Score (passed to server through ajax)
        
        console.log(id)
        console.log(val_num)
        console.log(msg)

        $.ajax({
            type: 'POST',
            url: my_url,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'rental_id': id,
                'score': val_num,
                'user_msg': msg,
            },

            // If transaction successful, give feedback and reload the current page
            success: function(result){
                console.log('RESPONSE WAS A SUCCESS'+result)
                window.location.reload()
            },

            //Otherwise, check if the error is caused by denied permission (Unauthenticated user i.e. not loged in)
            error: function(error){
                //if so, prompt user to login and redirect user to the current page after login
                if (error.status == 403) { 
                    if (confirm("You need to be loged in to Give feedback! Would you like to Login?")) {
                        top.location.href = '/login/?next=/'+id
                    } 
                    else {
                       return
                    }
                }
                //if error is not due to authentication error, console log the error
                console.log('AN ERROR OCCURED ERROR: '+error) 
            }
        })
    })
}




//===================================== BOOK HOSTEL SCRIPT ============================//

/* Get all booking form on the page marked as 'book-form' */
const formArray = Array.from(document.getElementsByClassName('book-form'));

/*  Loop through it all listening for the 'submit' activity
    if so, prevent submission and get data to be passed to server*/

for(let i=0; i<formArray.length; i++){
    let bookForm = formArray[i]
    let rental_id;
    let url;
    bookForm.addEventListener('submit', e =>{
        e.preventDefault()
        rental_id = e.target.id  //---------------------------> Rental id (passed to server through ajax)
        url = "/book/"+rental_id //---------------------------> url to handle post request

        $.ajax({
            type: 'post',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'rental_id':rental_id,
            },

            // If transaction successful, give feedback and reload the current page
            success: function(data){
                console.log('RESPONSE WAS A SUCCESS'+data)
                window.location.reload()
            },

            //Otherwise, check if the error is caused by denied permission (Unauthenticated user i.e. not loged in)
            error: function(error){
                if (error.status == 403) { 
                    //if so, prompt user to login
                    if (confirm("You need to be loged in to Book a rental! Would you like to Login?")) {
                        top.location.href = '/login/'
                    } 
                    else {
                       return
                    }
                }
                //if error is not due to authentication error, console log the error
                console.log('AN ERROR OCCURED ERROR: '+error)
            }
        })
    })
}

// ==================================== CANCEL BOOK RENTAL ========================//

const cancelFormArray = Array.from(document.getElementsByClassName('cancel-form'))


for(let i=0; i<cancelFormArray.length; i++){
    cancelForm = cancelFormArray[i]
    let rental_id;
    let url;

    cancelForm.addEventListener('submit', (e)=>{
        e.preventDefault()

        rental_id = e.target.id
        url = "/bookCancel/"+rental_id

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'rental_id':rental_id,
            },
            success: function(result){
                console.log('RESPONSE WAS A SUCCESS'+result)
            },
            error: function(error){
                console.log('AN ERROR OCCURED ERROR: '+error) 
                alert('AN ERROR OCCURED ERROR: '+error) 
            }
        })
        $(document).ajaxStop(function(){
            window.location.reload();
        });
    })
}