const API = "http://127.0.0.1:8000/students";

let currentPage = 1;
let currentSearch = "";
let limit = 15;
let isEdit = false;
let editMSSV = null;


/* ===== GPA & XẾP LOẠI ===== */
function tinhGPA(s) {
  const diem = [
    s.math_score,
    s.history_score,
    s.physics_score,
    s.chemistry_score,
    s.biology_score,
    s.english_score,
    s.geography_score
  ].map(d => {
    const num = Number(d);
    return isNaN(num) || num < 0 ? 0 : num;
  });

  const avg100 = diem.reduce((a, b) => a + b, 0) / diem.length;
  return +(avg100 / 10).toFixed(2);
}

function xepLoai(gpa) {
  if (gpa >= 8) return "Giỏi";
  if (gpa >= 6.5) return "Khá";
  if (gpa >= 5) return "Trung bình";
  return "Yếu";
}

/* ===== LOAD STUDENTS ===== */
async function loadStudents(page = 1) {
  let url = `${API}?page=${page}&limit=${limit}`;

  if (currentSearch) {
    url += `&search=${encodeURIComponent(currentSearch)}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();

    renderTable(data.data);
    renderPagination(data.total, data.page, data.limit);
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

/* ===== RENDER TABLE ===== */
function renderTable(students) {
  const tbody = document.querySelector("#studentTable tbody");
  tbody.innerHTML = "";

  if (!students || students.length === 0) {
    tbody.innerHTML = `<tr><td colspan="14">Không có dữ liệu</td></tr>`;
    return;
  }

  students.forEach(s => {
    const tr = document.createElement("tr");

    const gpa = tinhGPA(s);
    const rank = xepLoai(gpa);

    let rankClass = "";
    if (rank === "Giỏi") rankClass = "rank-gioi";
    else if (rank === "Khá") rankClass = "rank-kha";
    else if (rank === "Trung bình") rankClass = "rank-tb";
    else rankClass = "rank-yeu";

    tr.innerHTML = `
      <td>${s.mssv}</td>
      <td>${s.last_name ?? ""}</td>
      <td>${s.first_name ?? ""}</td>

      <td>${s.math_score ?? "-"}</td>
      <td>${s.history_score ?? "-"}</td>
      <td>${s.physics_score ?? "-"}</td>
      <td>${s.chemistry_score ?? "-"}</td>
      <td>${s.biology_score ?? "-"}</td>
      <td>${s.english_score ?? "-"}</td>
      <td>${s.geography_score ?? "-"}</td>

      <td>${gpa.toFixed(2)}</td>
      <td class="${rankClass}">${rank}</td>

      <td>
        <button onclick="viewDetail('${s.mssv}')">Xem</button>
      </td>
      <td>
        <button class="action edit" onclick='editStudent(${JSON.stringify(s)})'>Sửa</button>
        <button class="action delete" onclick="deleteStudent('${s.mssv}')">Xóa</button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}


/* ===== PAGINATION ===== */
function renderPagination(totalItems, page, pageLimit) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const totalPages = Math.ceil(totalItems / pageLimit);
  currentPage = page;

  const maxVisible = 5; // số nút hiển thị
  let start = Math.max(1, page - Math.floor(maxVisible / 2));
  let end = Math.min(totalPages, start + maxVisible - 1);

  if (start > 1) {
    pagination.appendChild(createPageBtn("«", 1));
    pagination.appendChild(createDots());
  }

  for (let i = start; i <= end; i++) {
    const btn = createPageBtn(i, i);
    if (i === page) btn.classList.add("active");
    pagination.appendChild(btn);
  }

  if (end < totalPages) {
    pagination.appendChild(createDots());
    pagination.appendChild(createPageBtn("»", totalPages));
  }
}

/* ===== HELPER ===== */
function createPageBtn(text, page) {
  const btn = document.createElement("button");
  btn.innerText = text;
  btn.onclick = () => loadStudents(page);
  return btn;
}

function createDots() {
  const span = document.createElement("span");
  span.innerText = "...";
  span.className = "dots";
  return span;
}


/* ===== SEARCH ===== */
document.getElementById("searchInput").addEventListener("input", e => {
  currentSearch = e.target.value.trim();
  loadStudents(1);
});

/* ===== DETAIL ===== */
async function viewDetail(mssv) {
  try {
    const res = await fetch(`${API}/${mssv}`);
    const s = await res.json();

    alert(
      `MSSV: ${s.mssv}\n` +
      `Họ: ${s.last_name}\n` +
      `Tên: ${s.first_name}\n` +
      `Email: ${s.email ?? "—"}\n` +
      `Giới tính: ${s.gender ?? "—"}\n` +
      `Nghề nghiệp: ${s.career_aspiration ?? "—"}`
    );
  } catch {
    alert("Không lấy được chi tiết sinh viên");
  }
}

/* ===== EDIT ===== */
function editStudent(s) {
  isEdit = true;
  editMSSV = s.mssv;
  mssv.disabled = true;

  Object.keys(s).forEach(k => {
    if (document.getElementById(k)) {
      document.getElementById(k).value = s[k] ?? "";
    }
  });
}


/* ===== DELETE ===== */
function deleteStudent(mssv) {
  if (!confirm("Xóa sinh viên này?")) return;
  fetch(`${API}/${mssv}`, { method: "DELETE" })
    .then(() => loadStudents());
}

/* ===== INIT ===== */
loadStudents();

function isValidScore(v) {
  if (v === null) return true; // cho phép bỏ trống
  return Number.isFinite(v) && v >= 0 && v <= 100;
}


/* ===== ADD / UPDATE ===== */
studentForm.onsubmit = function(e) {
  e.preventDefault();

  const student = {
    mssv: mssv.value.trim(),
    first_name: first_name.value.trim(),
    last_name: last_name.value.trim(),
    email: email.value.trim() || null,
    gender: gender.value || null,
    part_time_job: toBool(part_time_job.value),
    absence_days: absence_days.value ? Number(absence_days.value) : null,
    extracurricular_activities: toBool(extracurricular_activities.value),
    weekly_self_study_hours: weekly_self_study_hours.value ? Number(weekly_self_study_hours.value) : null,
    career_aspiration: career_aspiration.value || null,

    math_score: math_score.value ? Number(math_score.value) : null,
    history_score: history_score.value ? Number(history_score.value) : null,
    physics_score: physics_score.value ? Number(physics_score.value) : null,
    chemistry_score: chemistry_score.value ? Number(chemistry_score.value) : null,
    biology_score: biology_score.value ? Number(biology_score.value) : null,
    english_score: english_score.value ? Number(english_score.value) : null,
    geography_score: geography_score.value ? Number(geography_score.value) : null,
  };

  if (!student.mssv) {
    alert("MSSV không được để trống!");
    return;
  }

  const scoreFields = [
    "math_score","history_score","physics_score",
    "chemistry_score","biology_score","english_score","geography_score"
  ];

  for (const field of scoreFields) {
    const v = student[field];
    if (v !== null && (v < 0 || v > 100)) {
      alert(`❌ ${field} phải trong khoảng 0–100`);
      return;
    }
  }

  const method = isEdit ? "PUT" : "POST";
  const url = isEdit ? `${API}/${editMSSV}` : API;

  fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student)
  }).then(() => {
    resetForm();
    loadStudents();
  });
};


/* ===== RESET ===== */
function resetForm() {
  studentForm.reset();
  mssv.disabled = false;
  isEdit = false;
  editMSSV = null;
}



function toBool(v) {
  if (v === "") return null;
  return v === "true";
}

async function exportStudentsCSV() {
  try {
    const res = await fetch(`${API}/Allstudents`);
    const students = await res.json();

    if (!students.length) {
      alert("Không có dữ liệu");
      return;
    }

    // ===== HEADER CSV =====
    const headers = Object.keys(students[0]);

    // ===== BODY CSV =====
    const rows = students.map(s =>
      headers.map(h => {
        const v = s[h];
        return `"${v ?? ""}"`; // escape đơn giản
      }).join(",")
    );

    const csv = [
      headers.join(","),
      ...rows
    ].join("\n");

    // ===== DOWNLOAD =====
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "students.csv";
    a.click();

    URL.revokeObjectURL(url);

  } catch (e) {
    alert("Xuất CSV thất bại");
    console.error(e);
  }
}
