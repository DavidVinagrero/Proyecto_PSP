const API_ENDPOINT = "http://127.0.0.1:5000"; // Introducir aquí el endpoint de tu API

class RenderHTML {
  constructor() {
    this.getTodos();
    this.createTodo();
  }

  async getTodos() {
    const data = await fetch(API_ENDPOINT + "/get-todos").then((res) =>
      res.json()
    );
    console.log(data);
    let list = document.querySelector(".list-todos");
    data.forEach((element) => {
      let li = document.createElement("li");
      li.textContent = element.todo;
      list.append(li);
    });
    return data;
  }

  renderTodos(data) {}

  createTodo() {
    let button = document.querySelector("#add-todo-button");

    button.addEventListener("click", () => {
      let text = document.querySelector("#new-todo");
      fetch(API_ENDPOINT + "/create-todo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: text.value,
      })
        .then((res) => console.log(res))
        .catch((err) => console.error(err));
      text.value = "";
    });
  }
}

const renderer = new RenderHTML();
