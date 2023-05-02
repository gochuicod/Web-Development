let form = ''

const getCurrentStudent = data => {
    document.querySelector(".student_fullname").innerHTML = `<b>Edit |</b> ${data[1]} ${data[2]}`
    document.querySelector(".student_id").setAttribute("value",data[0])
}

const transferValue = data => form = data

document.querySelector('.confirmYes').addEventListener('click', () => document.querySelector(`.delete_${form}`).submit())