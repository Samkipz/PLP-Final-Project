
//=========================== STAR RATINGS ============================//

//get all stars
const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');


const form = document.querySelector('.rate-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

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


const handleSelect = (selection) => {
    switch(selection){
        case 'first':{
            handleStarSelect(0)
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
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

if (one) {
    const arr = [one, two, three, four, five]
    arr.forEach(item => item.addEventListener('mouseover', (event) =>{
        handleSelect(event.target.id)
    }))

    let val;
    arr.forEach(item => item.addEventListener('click', (event) =>{
        val = event.target.id
    }))
    form.addEventListener('submit', e=>{
        e.preventDefault()
        const my_url = "add_feedback"
        const id = e.target.id
        const msg = document.getElementById('msg').value
        const val_num = getNumericValue(val)
        
        console.log(id)
        console.log(val_num)
        console.log(msg)

        $.ajax({
            type: 'POST',
            url: my_url,//==================================? url to handle post request
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'rental_id': id,
                'score': val_num,
                'user_msg': msg,
            },
            success: function(result){
                console.log('RESPONSE WAS A SUCCESS'+result)
                window.location.reload()
            },
            error: function(error){
                if (error.status == 403) { 
                    if (confirm("You need to be loged in to Give feedback! Would you like to Login?")) {
                        // /login/?next=/2/add_feedback
                        top.location.href = '/login/?next=/'+id
                    } 
                    else {
                       return
                    }
                }
                console.log('AN ERROR OCCURED ERROR: '+error) 
            }
        })
    })
}

//=========================== BOOK HOSTEL ============================//


const formArray = Array.from(document.getElementsByClassName('book-form'));

for(let i=0; i<formArray.length; i++){
    let bookForm = formArray[i]
    let rental_id;
    let url;
    bookForm.addEventListener('submit', e =>{
        e.preventDefault()
        rental_id = e.target.id
        url = "/book/"+rental_id

        $.ajax({
            type: 'post',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'rental_id':rental_id,
            },
            success: function(data){
                console.log('RESPONSE WAS A SUCCESS'+data)
                window.location.reload()
            },
            error: function(error){
                if (error.status == 403) { 
                    if (confirm("You need to be loged in to Book a rental! Would you like to Login?")) {
                        top.location.href = '/login/'
                    } 
                    else {
                       return
                    }
                }
                console.log('AN ERROR OCCURED ERROR: '+error)
            }
        })
    })
}

// ======================== CANCEL BOOK RENTAL ==================/

const cancelFormArray = Array.from(document.getElementsByClassName('cancel-form'))

console.log(cancelFormArray)

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