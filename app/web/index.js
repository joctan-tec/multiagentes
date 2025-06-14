let previous_response_id;


const generateMessageElement = (message, sender) => {
  const container = document.createElement("div");
  container.classList.add(
    "flex",
    sender === "user" ? "justify-end" : "justify-start"
  );

  const messageBubble = document.createElement("div");
  messageBubble.textContent = message;

  // Estilos base
  messageBubble.classList.add(
    "p-3",
    "my-2",
    "max-w-[75%]",
    "rounded-lg",
    "shadow"
  );

  if (sender === "user") {
    messageBubble.classList.add("bg-blue-600", "text-white", "text-right");
  } else {
    messageBubble.classList.add("bg-gray-300", "text-black", "text-left");
  }

  container.appendChild(messageBubble);
  return container;
};

const createLoadingMessage = () => {
  const container = document.createElement("div");
  container.classList.add("flex", "justify-start");

  const messageBubble = document.createElement("div");
  messageBubble.classList.add(
    "p-3",
    "my-2",
    "max-w-[75%]",
    "rounded-lg",
    "shadow",
    "bg-gray-300",
    "text-black",
    "text-left",
    "loading-animation"
  );

  // Añadir puntos suspensivos animados
  messageBubble.innerHTML = `<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>`;

  container.appendChild(messageBubble);
  return { container, bubble: messageBubble };
};

const fetchChatGPTResponse = async (message) => {
  try {
    const response = await fetch("http://localhost:5000/chatgpt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, previous_response_id }),
    });

    if (!response.ok) {
      throw new Error("Error al obtener la respuesta de ChatGPT");
    }

    const data = await response.json();
    previous_response_id = data.previous_response_id; // Actualizar el ID de la respuesta previa
    console.log("Respuesta de ChatGPT:", data);
    return data.chatgpt_response;
  } catch (error) {
    console.error("Error al comunicarse con ChatGPT:", error);
    return "Lo siento, ocurrió un error al procesar tu mensaje.";
  }
};

// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.getElementById("messageInput");
  const maxRows = 7;

  textarea.addEventListener("input", () => {
    textarea.style.height = "auto"; // Reset height
    const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);
    const maxHeight = lineHeight * maxRows;

    textarea.style.height = `${textarea.scrollHeight}px`;

    if (textarea.scrollHeight > maxHeight) {
      textarea.style.height = `${maxHeight}px`;
      textarea.style.overflowY = "auto";
    } else {
      textarea.style.overflowY = "hidden";
    }
  });

  // Seleccionar el botón y el contenedor de la lista
  const messageForm = document.getElementById("messageForm");

  messageForm.addEventListener("submit", async function (event) {
    // Prevenir el comportamiento por defecto del formulario
    event.preventDefault();

    // Obtener el valor del campo de entrada
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;

    // Verificar si el mensaje no está vacío
    if (message.trim() !== "") {
      const messagesContainer = document.getElementById("messages");

      // Crear y agregar el mensaje del usuario
      const userMessageElement = generateMessageElement(message, "user");
      messagesContainer.appendChild(userMessageElement);
      console.log("Mensaje del usuario:", message);

      // Limpiar el campo de entrada
      messageInput.value = "";

      // Desplazar hacia abajo automáticamente
      messagesContainer.scrollTop = messagesContainer.scrollHeight;

      // Crear mensaje de carga
      const { container: loadingContainer, bubble: loadingBubble } =
        createLoadingMessage();
      messagesContainer.appendChild(loadingContainer);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;

      // Obtener respuesta
      await fetchChatGPTResponse(message)
        .then((chatgptResponse) => {
            // Parsear y mostrar la respuesta en HTML usando marked
            loadingBubble.innerHTML = marked.parse(chatgptResponse);
            loadingBubble.classList.remove("loading-animation");
            console.log("Respuesta de ChatGPT:", chatgptResponse);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch((error) => {
          console.error("Error al obtener la respuesta de ChatGPT:", error);
          loadingBubble.textContent =
            "Lo siento, ocurrió un error al procesar tu mensaje.";
          loadingBubble.classList.remove("loading-animation");
        });
    }
  });
});
