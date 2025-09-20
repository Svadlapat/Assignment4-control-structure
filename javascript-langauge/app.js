const express = require('express');
const { loadEmployees, scheduleWeek } = require('./scheduler');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/schedule', (req, res) => {
    const employees = loadEmployees('employee.csv');
    const schedule = scheduleWeek(employees);
    res.json(schedule);
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
