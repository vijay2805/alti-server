const express = require('express');
const router = express.Router();
const users = [];

// router.use(cors())

router.get('/', (req,res)=>{

    // console.log('req', req.headers)

    if(!req.headers['Authorization'] === 'Bearer fake-jwt-token')
    return JSON.stringify({ message: 'Unauthorized' });

res.send(users);
});

router.post('/login', (req,res)=>{
    const { username, password } = req.body;
    const user = users.find(x => x.username === username && x.password === password);
    res.send({...user,  token: 'fake-jwt-token'});
})

router.get('/:id', (req,res)=>{
const user = user.find(u=> u.id === parseInt(req.params.id));
if(!user) return res.status(404).send('The given user is not found');

res.send(user);
});

router.post('/',  (req,res)=>{
    const user = {
        firstname:req.body.firstName,
        lastname:req.body.lastName,
        username:req.body.username,
        password:req.body.password,
        email: req.body.email,
        country:req.body.country,
        gender:req.body.gender
    };
    user.id = users.length ? Math.max(...users.map(x => x.id)) + 1 : 1;
users.push(user);



res.send(user);

})


router.delete('/:id', (req, res)=>{
const user = users.find(u=>u.id===parseInt(req.params.id));
if(!user) return res.status(404).send("The given user not found");

const index = users.indexOf(user);
users.splice(index, 1);
res.send(user);
})

function ok(body) {
    resolve({ ok: true, text: () => Promise.resolve(JSON.stringify(body)) });
}

module.exports = router;