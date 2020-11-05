const express = require('express');
const users = require('./routes/user');
const cors = require('cors');
const app = express();
app.use(express.json());
app.use(cors())

app.use('/api/users',users );

const port = process.env.PORT || 7000;

app.listen(port, ()=>console.log(`Server running on Port ${port}`));