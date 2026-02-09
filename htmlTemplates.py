css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.chat-message .avatar-text {
    width: 78px;
    height: 78px;
    border-radius: 50%;
    background-color: #667085;
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}
.chat-message.bot .avatar-text {
    background-color: #2563eb;  /* Blue for bot */
}
.chat-message.user .avatar-text {
    background-color: #16a34a;  /* Green for user */
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <div class="avatar-text">BOT</div>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <div class="avatar-text">YOU</div>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
