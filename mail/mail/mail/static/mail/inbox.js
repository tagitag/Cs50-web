document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // when the compose form is submited, send the email
  document.querySelector('#compose-form').onsubmit = () => sendEmail();
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  let email_view = document.querySelector('#emails-view');
  email_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // load the emails for the given page
  fetch('emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {loadEmails(emails,email_view,mailbox)});
}

function sendEmail()
{
  
  // collect the important bits of the compose email
  let to = document.querySelector('#compose-recipients');
  let sub = document.querySelector('#compose-subject');
  let body = document.querySelector('#compose-body');
  
  // send the email using the email api 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify(
      {
        recipients: to.value ,
        subject: sub.value ,
        body: body.value ,
      }
    )
  })
  .then(response => {response.json()})
  .then(result => {console.log(result)});
  
  // load the sent page
  load_mailbox('sent');

  // prevent the page from refreshing
  return false;
  
}

// loads all the emails in the emails variable
function loadEmails(emails,email_view,mailbox)
{
  isSent = mailbox == 'sent'
  // make a unorerd list
  ul = document.createElement('ul');
  ul.classList.add('list-group');

  for(let i =0; i < emails.length; i++)
  {
    // make a li to hold each item 
    let li = document.createElement('li');
    
    //pause the animation 
    li.style.animationPlayState = 'paused';
    
    li.classList.add('list-group-item')

    // make a div to store the informatio that goes in the list
    let div = document.createElement('div');
    
    // allow for \n to work
    div.style.whiteSpace = 'pre';


    // add information to the div
    
    if (isSent)
    {
      div.innerHTML = `<b>To:</b> ${emails[i].recipients[0]} \n<b>Subject:</b> ${emails[i].subject} \n<b>Sent:</b> ${emails[i].timestamp}`
    }
    else
    {
      div.innerHTML = `<b>From:</b> ${emails[i].recipients[0]} \n<b>Subject:</b> ${emails[i].subject} \n<b>Sent:</b> ${emails[i].timestamp}`
    }
    
    if (emails[i].read && !isSent)
    {
      li.style.backgroundColor = 'gray';
    }
    li.style.paddingBottom = '2px';
    li.style.paddingTop = '2px';
    

    div.addEventListener('click', () => {Read(emails[i].id)})

    // add the div to the li
    li.appendChild(div)

    // generate a button to archive the specific file 
    if (!isSent)
    {
      var btn = document.createElement('button');
      btn.classList.add('btn');
      btn.classList.add('btn-primary');
      btn.classList.add('leftSide');
      btn.innerHTML = '<img src=/static/mail/envelope-open-fill.svg>';
      btn.onclick = () => {archive(emails[i].id, emails[i].archived, li)};
    }

    // if a button is made append it to the list 
    btn ? li.appendChild(btn) : console.log(23);

    // append the li to the ul element 
    ul.appendChild(li);
  }
  // apend the ul element to the email_view
  email_view.appendChild(ul);
}

// displays the email when clicked, also updates the .read bool to True
function Read(id)
{
  // hide the other views and show read-view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';

  // get the email 
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => ReadEmail(email));


  //update the value of the read bool to True
  fetch('/emails/' + id, {method:'PUT', body:JSON.stringify({read:true})})
}

function ReadEmail(email)
{
  // collect the needed elements from the DOM
  to = document.querySelector('#read-to');
  from = document.querySelector('#read-from');
  subject = document.querySelector('#read-subject');
  body = document.querySelector('#read-body');
  replybtn = document.querySelector('#read-reply');

  // add a event handler to the reply btn
  replybtn.onclick = () => {Reply(email)};
  // enable white space for the body
  body.style.whiteSpace = 'pre';

  // input the information in the needed elements
  console.log(email);
  to.innerHTML = 'To: ' + email.recipients;
  from.innerHTML = 'From: ' +  email.sender;
  subject.innerHTML = email.subject;
  body.innerHTML = email.body;
}


// when run it will archive or de-archive the email with the given id
function archive(id,archived,li)
{
  if (archived)
  {
    fetch('/emails/' + id, {method:'PUT', body:JSON.stringify({archived:false})})
  }
  else
  {
    fetch('/emails/' + id, {method:'PUT', body:JSON.stringify({archived:true})})
  }

  // run animation to make the li element disapear:
  li.style.animationPlayState = 'running';
  setTimeout(() => {li.remove()}, 2000);
}

// reply to a email
function Reply(email)
{
  // load the compose view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  //auto fill the compose view
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.substring(0,4) == 'Re: ' ? email.subject :'Re: ' + email.subject;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} Wrote:\n${email.body}\n`;

}