(function() {
    function initTemplates() {
        // Find the element with id_content
        const textarea = document.getElementById('id_content');
        if (!textarea) return;

        // Check if we already injected the selector
        if (document.getElementById('report-template-selector')) return;

        // Predefined templates
        const templates = {
            "": "--- Select an Orthopedic Template ---",
            "knee": `<h3>KNEE ASSESSMENT REPORT</h3>
<p><strong>Chief Complaint:</strong> Pain and instability in the [Left/Right] knee for [Duration].</p>
<p><strong>Clinical Examination:</strong></p>
<ul>
  <li>Range of Motion (ROM): [Flexion / Extension]</li>
  <li>Joint Line Tenderness: [Medial / Lateral]</li>
  <li>Lachman Test: [Positive / Negative / Grade]</li>
  <li>Anterior Drawer: [Positive / Negative]</li>
  <li>McMurray Test: [Positive / Negative]</li>
</ul>
<p><strong>Imaging (X-Ray / MRI) Findings:</strong> [Detail findings here]</p>
<p><strong>Diagnosis:</strong> [e.g., ACL Tear / Meniscus Tear / Osteoarthritis]</p>
<p><strong>Treatment Plan:</strong> [e.g., Arthroscopic Reconstruction / Physiotherapy / TKA]</p>`,
            "hip": `<h3>HIP ASSESSMENT REPORT</h3>
<p><strong>Chief Complaint:</strong> Deep groin pain and stiffness in the [Left/Right] hip, worsening with weight-bearing.</p>
<p><strong>Clinical Examination:</strong></p>
<ul>
  <li>Gait: [Antalgic / Normal]</li>
  <li>Range of Motion (ROM): Internal Rotation: [Deg / Normal], External Rotation: [Deg / Normal]</li>
  <li>Trendelenburg Sign: [Positive / Negative]</li>
</ul>
<p><strong>Imaging Findings:</strong> [Joint space narrowing / Osteophytes / Subchondral cysts]</p>
<p><strong>Diagnosis:</strong> [e.g., Hip Osteoarthritis / Avascular Necrosis (AVN)]</p>
<p><strong>Treatment Plan:</strong> [e.g., Conservative Management / Total Hip Arthroplasty (THA)]</p>`,
            "shoulder": `<h3>SHOULDER ASSESSMENT REPORT</h3>
<p><strong>Chief Complaint:</strong> Pain and overhead weakness in the [Left/Right] shoulder.</p>
<p><strong>Clinical Examination:</strong></p>
<ul>
  <li>Active Abduction: [Range of motion]</li>
  <li>Neer Impingement Sign: [Positive / Negative]</li>
  <li>Hawkins-Kennedy Test: [Positive / Negative]</li>
  <li>Empty Can Test (Supraspinatus): [Positive / Negative]</li>
</ul>
<p><strong>Imaging Findings:</strong> [Detail MRI / Ultrasound findings]</p>
<p><strong>Diagnosis:</strong> [e.g., Rotator Cuff Tear / Impingement Syndrome / Frozen Shoulder]</p>
<p><strong>Treatment Plan:</strong> [e.g., Subacromial Decompression / Cuff Repair / Physical Therapy]</p>`,
            "spine": `<h3>SPINE & LOWER BACK CONSULTATION</h3>
<p><strong>Chief Complaint:</strong> Lower back pain radiating to [Left/Right] lower limb for [Duration].</p>
<p><strong>Clinical Examination:</strong></p>
<ul>
  <li>Straight Leg Raise (SLR) Test: [degrees / Positive / Negative]</li>
  <li>Reflexes: Knee: [Normal / Sluggish], Ankle: [Normal / Sluggish]</li>
  <li>Motor Strength: [Grade 5/5 or specify weakness]</li>
</ul>
<p><strong>Imaging Findings:</strong> [Disk herniation / Canal stenosis at L4-L5 / L5-S1]</p>
<p><strong>Diagnosis:</strong> [e.g., Lumbar Radiculopathy / Sciatica / Herniated Disc]</p>
<p><strong>Treatment Plan:</strong> [e.g., Epidural Steroid Injection / Decompression / Physiotherapy]</p>`
        };

        // Create container for dropdown
        const container = document.createElement('div');
        container.style.marginBottom = '15px';
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.gap = '10px';
        container.style.marginTop = '10px';

        const label = document.createElement('label');
        label.innerText = 'Load Orthopedic Template:';
        label.style.fontWeight = 'bold';
        label.style.fontSize = '13px';
        label.className = 'text-gray-700 dark:text-gray-300';

        const select = document.createElement('select');
        select.id = 'report-template-selector';
        // Unfold style classes for premium styling:
        select.className = 'border border-gray-300 dark:border-gray-700 rounded-md bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-2 text-sm focus:border-primary-500 focus:ring-primary-500 min-w-[250px]';

        for (const [key, labelText] of Object.entries(templates)) {
            const opt = document.createElement('option');
            opt.value = key;
            if (key === "") {
                opt.innerText = labelText;
            } else {
                opt.innerText = labelText.split('\n')[0].replace('<h3>', '').replace('</h3>', '');
            }
            select.appendChild(opt);
        }

        container.appendChild(label);
        container.appendChild(select);

        // Insert container before the CKEditor element
        const cke = document.getElementById('cke_id_content');
        if (cke) {
            cke.parentNode.insertBefore(container, cke);
        } else {
            const parent = textarea.parentNode;
            parent.insertBefore(container, textarea);
        }

        select.addEventListener('change', function() {
            const selectedKey = select.value;
            if (!selectedKey) return;

            const htmlContent = templates[selectedKey];

            if (window.CKEDITOR && window.CKEDITOR.instances && window.CKEDITOR.instances.id_content) {
                window.CKEDITOR.instances.id_content.setData(htmlContent);
            } else {
                textarea.value = htmlContent;
            }
        });
    }

    // Wait for CKEditor to be ready or document loaded
    if (window.CKEDITOR) {
        if (window.CKEDITOR.instances && window.CKEDITOR.instances.id_content) {
            initTemplates();
        } else {
            window.CKEDITOR.on('instanceReady', function(evt) {
                if (evt.editor.name === 'id_content') {
                    initTemplates();
                }
            });
        }
    } else {
        document.addEventListener('DOMContentLoaded', initTemplates);
    }
})();
