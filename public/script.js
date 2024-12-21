document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("dataForm")
    .addEventListener("submit", async function (event) {
      event.preventDefault();
    //   event.defaultPrevented();

      const age = parseInt(document.getElementById("age").value || 0);
      const pclass = parseInt(document.getElementById("pclass").value || 0);
      const fare = parseInt(document.getElementById("fare").value || 0);
      const sex = parseInt(document.getElementById("sex").value || 0);
      const port = document.getElementById("port").value || 'S';

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
});
