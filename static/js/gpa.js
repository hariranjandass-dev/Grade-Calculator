/* gpa.js — GradeTrack, Annamalai University grading */
'use strict';

// GRADE_SCALES injected by template. Fallback = AU default.
if (typeof GRADE_SCALES === 'undefined' || !GRADE_SCALES || !GRADE_SCALES.length) {
    var GRADE_SCALES = [
        { grade: 'S',  min: 90, max: 100, point: 10 },
        { grade: 'A',  min: 80, max: 89,  point: 9  },
        { grade: 'B',  min: 70, max: 79,  point: 8  },
        { grade: 'C',  min: 60, max: 69,  point: 7  },
        { grade: 'D',  min: 55, max: 59,  point: 6  },
        { grade: 'E',  min: 50, max: 54,  point: 5  },
        { grade: 'RA', min: 0,  max: 49,  point: 0  },
    ];
}

function getGradeFromMarks(marks) {
    var m = parseFloat(marks);
    if (isNaN(m) || m < 0 || m > 100) return { grade: '', point: '' };
    for (var i = 0; i < GRADE_SCALES.length; i++) {
        if (m >= GRADE_SCALES[i].min && m <= GRADE_SCALES[i].max) {
            return { grade: GRADE_SCALES[i].grade, point: GRADE_SCALES[i].point };
        }
    }
    return { grade: 'RA', point: 0 };
}

function updateGradeRow(row) {
    var marksInput   = row.querySelector('.marks-input');
    var gradeDisplay = row.querySelector('.grade-display');
    var pointDisplay = row.querySelector('.points-display');
    if (!marksInput) return;
    var val = marksInput.value.trim();
    if (val === '') {
        gradeDisplay.value = '';
        pointDisplay.value = '';
        return;
    }
    var result = getGradeFromMarks(val);
    gradeDisplay.value = result.grade;
    pointDisplay.value = result.point;

    // Highlight RA
    gradeDisplay.style.color = (result.grade === 'RA') ? '#dc3545' : '';
    gradeDisplay.style.fontWeight = 'bold';
}

function updateTotalCredits() {
    var inputs = document.querySelectorAll('#subjectBody input[name="credits[]"]');
    var total = 0;
    inputs.forEach(function(i) {
        var v = parseFloat(i.value);
        if (!isNaN(v) && v > 0) total += v;
    });
    var el = document.getElementById('totalCredits');
    if (el) el.textContent = total > 0 ? total : '—';
}

function makeRow(hasCodeCol) {
    if (hasCodeCol) {
        return '<tr class="subject-row">' +
            '<td><input type="text" name="subject_name[]" class="form-control form-control-sm" placeholder="e.g. Mathematics – I" required></td>' +
            '<td><input type="text" name="subject_code[]" class="form-control form-control-sm" placeholder="e.g. 22ETBS101"></td>' +
            '<td><input type="number" name="credits[]" class="form-control form-control-sm" value="3" min="0.5" step="0.5" required></td>' +
            '<td><input type="number" name="marks[]" class="form-control form-control-sm marks-input" placeholder="0–100" min="0" max="100" step="0.01"></td>' +
            '<td><input type="text" class="form-control form-control-sm grade-display" readonly tabindex="-1" style="background:#f8f9fa;font-weight:bold"></td>' +
            '<td><input type="number" class="form-control form-control-sm points-display" readonly tabindex="-1" style="background:#f8f9fa"></td>' +
            '<td><button type="button" class="btn btn-outline-danger btn-sm remove-row"><i class="bi bi-trash"></i></button></td>' +
            '</tr>';
    }
    return '<tr class="subject-row">' +
        '<td><input type="text" name="subject_name[]" class="form-control form-control-sm" placeholder="e.g. Mathematics – I" required></td>' +
        '<td><input type="number" name="credits[]" class="form-control form-control-sm" value="4" min="0.5" step="0.5" required></td>' +
        '<td><input type="number" name="marks[]" class="form-control form-control-sm marks-input" placeholder="0–100" min="0" max="100" step="0.01"></td>' +
        '<td><input type="text" class="form-control form-control-sm grade-display" readonly tabindex="-1" style="background:#f8f9fa;font-weight:bold"></td>' +
        '<td><input type="number" class="form-control form-control-sm points-display" readonly tabindex="-1" style="background:#f8f9fa"></td>' +
        '<td><button type="button" class="btn btn-outline-danger btn-sm remove-row"><i class="bi bi-trash"></i></button></td>' +
        '</tr>';
}

function populateGradeScaleTable() {
    var tbody = document.getElementById('gradeScaleTable');
    if (!tbody) return;
    tbody.innerHTML = GRADE_SCALES.map(function(s) {
        var badge = s.grade === 'RA' ? 'bg-danger' :
                    s.point >= 9  ? 'bg-success' :
                    s.point >= 8  ? 'bg-primary' :
                    s.point >= 7  ? 'bg-info text-dark' :
                    s.point >= 6  ? 'bg-warning text-dark' : 'bg-secondary';
        return '<tr><td>' + s.min + ' – ' + s.max + '</td>' +
               '<td><span class="badge ' + badge + '">' + s.grade + '</span></td>' +
               '<td><strong>' + s.point + '</strong></td></tr>';
    }).join('');
}

document.addEventListener('DOMContentLoaded', function () {
    var body   = document.getElementById('subjectBody');
    var addBtn = document.getElementById('addSubject');

    if (!body) return;

    // Detect if this page has a subject_code column
    var hasCodeCol = !!body.querySelector('input[name="subject_code[]"]');

    populateGradeScaleTable();

    // Init all existing rows
    body.querySelectorAll('.subject-row').forEach(updateGradeRow);
    updateTotalCredits();

    // Live: marks typed → grade auto-fills
    body.addEventListener('input', function(e) {
        if (e.target.classList.contains('marks-input')) {
            updateGradeRow(e.target.closest('.subject-row'));
        }
        if (e.target.name === 'credits[]') {
            updateTotalCredits();
        }
    });

    // Add row button
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            body.insertAdjacentHTML('beforeend', makeRow(hasCodeCol));
            updateTotalCredits();
            // Focus the new subject name field
            var rows = body.querySelectorAll('.subject-row');
            var lastRow = rows[rows.length - 1];
            var nameInput = lastRow.querySelector('input[name="subject_name[]"]');
            if (nameInput) nameInput.focus();
        });
    }

    // Remove row (event delegation)
    body.addEventListener('click', function(e) {
        var btn = e.target.closest('.remove-row');
        if (!btn) return;
        var rows = body.querySelectorAll('.subject-row');
        if (rows.length > 1) {
            btn.closest('.subject-row').remove();
            updateTotalCredits();
        } else {
            // Clear the last row instead of removing it
            var row = btn.closest('.subject-row');
            row.querySelectorAll('input[type="text"], input[type="number"]').forEach(function(inp) {
                if (!inp.readOnly) inp.value = inp.name === 'credits[]' ? '4' : '';
            });
            row.querySelector('.grade-display').value = '';
            row.querySelector('.points-display').value = '';
            updateTotalCredits();
        }
    });
});
