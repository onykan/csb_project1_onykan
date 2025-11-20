// A script to make the view scroll to the reply text area when the side bar button is pressed
addEventListener("DOMContentLoaded", (event) => {
    const button = document.getElementById("sbreplybutton");
    const replyElement = document.getElementById("replyelement");

    button.addEventListener("click", () => {
        replyElement.scrollIntoView();
        replyTextArea = document.getElementById("reply_text");
        if (replyTextArea) replyTextArea.focus();
    });
});