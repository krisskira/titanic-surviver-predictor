document.addEventListener("DOMContentLoaded", () => {
  const _chats = [];

  function insertMessages(chats = []) {
    const chatList = document.getElementById("chatList");
    chatList.innerHTML = "";
    for (const chat of chats) {
      const rol = chat.rol;
      if (rol === "user") {
        chat.className = "list-group-item list-group-item-primary";
      } else {
        chat.className = "list-group-item list-group-item-secondary";
      }
      const listItem = document.createElement("li");
      listItem.className = "list-group-item";
      listItem.textContent = chat.message;
      chatList.appendChild(listItem);
    }
  }

  function initChat() {
    document
      .getElementById("sendMessageButton")
      .addEventListener("click", async function (event) {
        event.preventDefault();

        try {
          const chatInput = document.getElementById("chatInput");

          const response = await fetch("http://localhost:8000/api/v1/chat", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: chatInput.value }),
          });

          const data = await response.json();

          _chats.push({
            rol: "user",
            message: chatInput.value,
          });

          _chats.push({
            rol: "ai",
            message: data.message,
          });
          chatInput.value = "";
          insertMessages(_chats);
        } catch (error) {
          responseMessage.textContent =
            "Error submitting the form. Please try again.";
          responseMessage.className = "alert alert-danger";
          responseMessage.style.display = "block";

          setTimeout(() => {
            responseMessage.style.display = "none";
          }, 10000);
        }
      });
  }

  function initForm() {
    document
      .getElementById("dataForm")
      .addEventListener("submit", async function (event) {
        event.preventDefault();
        //   event.defaultPrevented();

        const age = parseInt(document.getElementById("age").value || 0);
        const pclass = parseInt(document.getElementById("pclass").value || 0);
        const fare = parseInt(document.getElementById("fare").value || 0);
        const sex = parseInt(document.getElementById("sex").value || 0);
        const port = document.getElementById("port").value || "S";

        const responseMessage = document.getElementById("responseMessage");

        try {
          const response = await fetch("http://localhost:8000/api/v1/predict", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ age, pclass, fare, sex, port }),
          });

          const data = await response.json();

          if (data.result === true) {
            responseMessage.textContent = "Sobrevive";
            responseMessage.className = "alert alert-success";
          } else {
            responseMessage.textContent = "No sobrevive";
            responseMessage.className = "alert alert-danger";
          }

          responseMessage.style.display = "block";

          setTimeout(() => {
            responseMessage.style.display = "none";
          }, 10000);
        } catch (error) {
          responseMessage.textContent =
            "Error submitting the form. Please try again.";
          responseMessage.className = "alert alert-danger";
          responseMessage.style.display = "block";

          setTimeout(() => {
            responseMessage.style.display = "none";
          }, 10000);
        }
      });
  }

  initChat();
  initForm();
});
