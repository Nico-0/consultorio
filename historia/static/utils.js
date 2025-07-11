
export function toggle(idElement) {
    return function() {
        let element = document.getElementById(idElement)
        if(element.style.visibility == 'hidden')
            element.style = 'visibility: visible; position: initial'
        else
            element.style = 'visibility: hidden; position: absolute'
    };
}
