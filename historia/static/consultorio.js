console.log('consultorio.js')
import { toggle } from './utils.js';


document.getElementById("nuevoPaciente").addEventListener("click", toggle('cargaPaciente'));

document.getElementById("buscador").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    var inputString = this.value; //value from the input field
    let url = new URL(window.location.href);
    url.searchParams.delete("search");
    url.searchParams.set("search", inputString);

    window.location.href = url.toString();
  }
});