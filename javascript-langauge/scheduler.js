const fs = require('fs');

const DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
const SHIFTS = ["morning","afternoon","evening"];
const MIN_PER_SHIFT = 2;
const MAX_DAYS_PER_EMP = 5;

// Load employees from CSV with preference rankings
function loadEmployees(filename) {
    const data = fs.readFileSync(filename, 'utf-8');
    const lines = data.trim().split('\n');
    const header = lines.shift().split(',');
    let employees = {};
    for (const line of lines) {
        const row = line.split(',');
        const name = row[0];
        employees[name] = {};
        for (let i = 1; i < header.length; i++) {
            employees[name][header[i]] = row[i].split('>');
        }
    }
    return employees;
}

// Scheduler with priority + balancing
function scheduleWeek(employees) {
    const schedule = {};
    const assignments = {};
    for (let name in employees) assignments[name] = new Set();

    for (let day of DAYS) {
        schedule[day] = {morning: [], afternoon: [], evening: []};
        const assignedToday = new Set();

        // --- First pass: assign 1 per shift (based on preference) ---
        for (let shift of SHIFTS) {
            const candidates = Object.keys(employees)
                .filter(name => !assignedToday.has(name) && assignments[name].size < MAX_DAYS_PER_EMP)
                .map(name => {
                    const prefIndex = employees[name][day].indexOf(shift);
                    return {name, prefIndex};
                })
                .filter(c => c.prefIndex >= 0)
                .sort((a,b) => a.prefIndex - b.prefIndex);

            if (candidates.length > 0) {
                const c = candidates[0]; // best candidate
                schedule[day][shift].push(c.name);
                assignedToday.add(c.name);
                assignments[c.name].add(day);
            }
        }

        // --- Second pass: ensure 2 per shift (fill shortages) ---
        for (let shift of SHIFTS) {
            while (schedule[day][shift].length < MIN_PER_SHIFT) {
                // pool of people under 5 days and not already on this shift
                const pool = Object.keys(employees)
                    .filter(n => assignments[n].size < MAX_DAYS_PER_EMP && !schedule[day][shift].includes(n));

                if (pool.length === 0) break; // no more eligible
                const choice = pool[Math.floor(Math.random() * pool.length)];
                schedule[day][shift].push(choice);
                assignments[choice].add(day);
                assignedToday.add(choice);
            }
        }
    }

    return schedule;
}

module.exports = { loadEmployees, scheduleWeek };
