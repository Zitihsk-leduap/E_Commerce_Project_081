console.log("hello world")

var updateBtns=document.getElementsByClassName('update-cart')
for(i=0;i<updateBtns.length;i++)
{
  updateBtns[i].addEventListener('click',function(){
    var productId=this.dataset.product
    var action=this.dataset.action
    console.log('productId:',productId,'Action:',action)


    console.log('USER:',user)
    if(user=='AnonymousUser'){
      console.log('User is not authenticated')
    }
    else{
      console.log('User is authenticated')
      updateuserorder(productId,action)
      
    }
  })
}

function updateuserorder(productId,action) {
  console.log('User is authenticated,sending the data.....')
  
  var url='/update_item/'

  fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, // Ensure `csrftoken` variable is defined
    },
    body: JSON.stringify({'productId': productId, 'action': action})
})
.then((response) => {
    return response.json();
})
.then((data) => {
    console.log('Data:', data);
    location.reload();
})
.catch((error) => {
    console.error('Error:', error);
});

}

