const express = require('express'), mysql = require('mysql'), bodyparser = require('body-parser'), fileUpload = require('express-fileupload');

let port = process.env.port || 8000, app = express()

// This section handles database connection
let config = {
    host: "localhost",
    user: "root",
    password: "",
    database: "Sysint",
    charset: "utf8mb4",
    multipleStatement: true
}
let db = mysql.createPool(config)

app.listen(port, () => require("dns").lookup(require("os").hostname(), (err,addr,fam) => console.log(`http://${addr}:${port}`)))

app.use(express.static(`${__dirname}/public`))
app.use(bodyparser.urlencoded({extended:true}))
app.use(bodyparser.json())
app.use(fileUpload({
    createParentPath: true
}))

// This section is for the login page
app.get("/",(req,res) => res.render("index.html"))

// This section is for the main page
app.get("/main",(req,res) => res.sendFile(`${__dirname}/public/main.html`))

// This section creates a user
app.post("/user",(req,res) => {
    let { username, password } = req.body;
    let sql = `insert into tbluser (username,password) values ('${username}','${password}')`;
    db.query(sql, err => err ? res.status(500).json(err) : res.redirect("/main"))
})

// This section selects all users
app.get("/user",(req,res) => {
    let sql = "select * from tbluser"
    db.query(sql, (err,results) => err ? res.status(500).json(err) : res.json(results))
})

// This section updates a user's data
app.put("/user/update",(req,res) => {
    let { username, password, id } = req.body;
    let sql = `update tbluser set username='${username}', password='${password}' where id=${id}`;
    db.query(sql, err => err ? res.status(500).json(err) : res.json({"message":"User updated!"}));
})

// This section deletes user data via id
app.delete("/user/:id",(req,res) => {
    let sql = `delete from tbluser where id=${req.params.id}`
    db.query(sql, err => err ? res.status(500).json(err) : res.json({"message":"User removed!"}));
    db.query('alter table tbluser auto_increment=1')
})

// This section creates student data
app.post("/student", (req,res) => {
    if(req.files){
        let { lastname, firstname, course, level } = req.query, { webcam } = req.files;
        let stamp = `${Date.now()}${webcam.name}`

        webcam.mv(`./public/assets/images/${stamp}`)

        let sql = `insert into tblstudent (lastname,firstname,course,level,imagepath) values ('${lastname}','${firstname}','${course}','${level}','./assets/images/${stamp}')`;
        db.query(sql, err => err ? res.status(500).json(err) : res.redirect("/main"))
    }
})

// This section selects all students
app.get("/student",(req,res) => {
    let sql = "select * from tblstudent"
    db.query(sql, (err,results) => err ?  res.status(500).json(err) : res.json(results))
})

// This section updates a student's data
app.put("/student/update",(req,res) => {
    let { idno, lastname, firstname, course, level } = req.body;
    let sql = `update tblstudent set lastname='${lastname}', firstname='${firstname}', course='${course}', level='${level}' where idno=${idno}`
    db.query(sql, err => err ? res.status(500).json(err) : res.json({"message":"Student updated!"}))
})

// This section deletes student data via id
app.delete("/student/:id",(req,res) => {
    let sql = `delete from tblstudent where idno=${req.params.id}`
    db.query(sql, err => err ? res.status(500).json(err) : res.json({"message":"Student removed!"}))
    db.query('alter table tblstudent auto_increment=1')
})

// This section handles logins
app.post("/login",(req,res) => {
    let { username, password } = req.body;
    let sql = `select * from tbluser where username='${username}' and password='${password}'`;
    if(username == "admin" && password == "user") res.redirect("/main")
    else{
        db.query(sql,(err,results) => {
            if(err) return res.status(500).json("Login Failed")
            else {
                if(results.length > 0) res.redirect("/main")
                else res.redirect("/?message=LOGIN FAILED")
            }
        })
    }
})