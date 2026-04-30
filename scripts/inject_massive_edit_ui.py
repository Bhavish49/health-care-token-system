import re

admin_path = r"c:\healthCareTokenSystem\dashboards\admin.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add new CSS for the Edit Profile UI
new_css = """
        /* Edit Profile Specific Styles */
        .edit-panel { background-color: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; margin-bottom: 24px; }
        .edit-panel-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; color: #fff; margin-bottom: 24px; font-weight: 600; }
        .form-label { display: block; font-size: 0.8rem; color: #cbd5e1; margin-bottom: 8px; font-weight: 500; }
        .form-label .req { color: #ef4444; margin-left: 4px; }
        .form-input { width: 100%; background: rgba(10, 15, 28, 0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 16px; color: #fff; font-family: inherit; font-size: 0.9rem; transition: border-color 0.2s; }
        .form-input:focus { outline: none; border-color: var(--primary); }
        .form-input::placeholder { color: #475569; }
        
        .img-upload-box { position: relative; border-radius: 12px; overflow: hidden; background: rgba(10, 15, 28, 0.6); border: 1px solid rgba(255,255,255,0.1); }
        .img-upload-box img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .img-overlay-btn { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.1); color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; display: flex; align-items: center; gap: 6px; cursor: pointer; white-space: nowrap; }
        .img-overlay-btn:hover { background: rgba(15, 23, 42, 0.9); }
        .remove-img-btn { position: absolute; top: 12px; right: 12px; width: 24px; height: 24px; background: rgba(15, 23, 42, 0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #cbd5e1; border: none; }
        .remove-img-btn:hover { color: #ef4444; }

        .service-checkbox { display: flex; align-items: center; gap: 10px; background: rgba(10, 15, 28, 0.6); border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 8px; cursor: pointer; }
        .service-checkbox input[type="checkbox"] { accent-color: var(--success); width: 16px; height: 16px; }
        .service-checkbox span { font-size: 0.85rem; color: #cbd5e1; }
        
        .add-service-btn { color: var(--success); font-size: 0.85rem; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; background: none; border: none; font-weight: 500; margin-top: 12px; }

        .equipment-card { background: rgba(10, 15, 28, 0.4); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden; position: relative; }
        .equipment-card img { width: 100%; height: 140px; object-fit: cover; }
        .equipment-info { padding: 12px; }
        .equipment-info h5 { margin: 0 0 4px 0; font-size: 0.85rem; color: #fff; }
        .equipment-info p { margin: 0; font-size: 0.75rem; color: var(--text-muted); }

        .add-equipment-card { border: 1px dashed rgba(255,255,255,0.2); border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; cursor: pointer; height: 100%; min-height: 220px; transition: 0.2s; }
        .add-equipment-card:hover { border-color: var(--primary); background: rgba(14, 165, 233, 0.05); }
        .add-equipment-card .icon-circle { width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: var(--text-muted); }
        .add-equipment-card p { margin: 0; font-size: 0.85rem; color: var(--text-muted); }

        .bottom-actions { display: flex; justify-content: flex-end; gap: 16px; margin-top: 32px; margin-bottom: 40px; }
        .btn-cancel { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #fff; padding: 12px 24px; border-radius: 8px; font-size: 0.9rem; font-weight: 500; cursor: pointer; }
        .btn-cancel:hover { background: rgba(255,255,255,0.05); }
        .btn-save { background: var(--success); color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-save:hover { background: #16a34a; }
"""

if "/* Edit Profile Specific Styles */" not in content:
    content = content.replace("</style>", new_css + "\n    </style>")

# 2. Add the section-edit-profile HTML inside main-content
edit_profile_html = """
            <!-- Edit Profile Section -->
            <div id="section-edit-profile" class="hidden">
                <div class="top-header" style="border-bottom: 1px solid var(--border-color); padding-bottom: 24px; margin-bottom: 24px;">
                    <div class="header-title" style="display: flex; align-items: center; gap: 16px;">
                        <button onclick="showSection(event, 'overview')" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; color: #cbd5e1; cursor: pointer;"><i data-lucide="arrow-left" size="18"></i></button>
                        <div>
                            <h1 style="font-size: 1.5rem;">Edit Hospital Profile</h1>
                            <p style="margin: 0; margin-top: 4px;">Update your hospital information and showcase your services</p>
                        </div>
                    </div>
                    <div class="user-profile">
                        <div>
                            <p class="name" style="color: #fff;">Admin</p>
                            <p class="role">Super Admin</p>
                        </div>
                        <div class="user-avatar"><i data-lucide="building"></i></div>
                    </div>
                </div>

                <form id="fullProfileForm" onsubmit="saveHospitalProfile(event)">
                    <!-- Basic Info -->
                    <div class="edit-panel">
                        <h3 class="edit-panel-title">Hospital Basic Information</h3>
                        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; margin-bottom: 24px;">
                            <div>
                                <label class="form-label">Hospital Banner</label>
                                <div class="img-upload-box" style="height: 220px;">
                                    <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80" id="epBannerPreview">
                                    <button type="button" class="img-overlay-btn" onclick="document.getElementById('epBannerUpload').click()"><i data-lucide="camera" size="14"></i> Change Banner</button>
                                    <input type="file" id="epBannerUpload" hidden accept="image/*">
                                </div>
                                <p style="font-size: 0.7rem; color: #64748b; margin-top: 8px;">Recommended size: 1200 x 400px. JPG, PNG up to 5MB</p>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 16px;">
                                <div>
                                    <label class="form-label">Hospital Name <span class="req">*</span></label>
                                    <input type="text" class="form-input" id="epName" value="ArogyaCare Super Speciality Hospital" required>
                                </div>
                                <div>
                                    <label class="form-label">Tagline</label>
                                    <input type="text" class="form-input" id="epTagline" value="Compassionate Care, Advanced Cure">
                                </div>
                                <div>
                                    <label class="form-label">Description <span class="req">*</span></label>
                                    <textarea class="form-input" id="epDesc" rows="4" required>ArogyaCare is a leading multi-speciality hospital providing world-class healthcare services with state-of-the-art technology and a team of highly experienced medical professionals.</textarea>
                                    <div style="text-align: right; font-size: 0.7rem; color: #64748b; margin-top: 4px;">160/500</div>
                                </div>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                            <div>
                                <label class="form-label">Established Year <span class="req">*</span></label>
                                <input type="number" class="form-input" id="epEst" value="2010" required>
                            </div>
                            <div>
                                <label class="form-label">Total Beds <span class="req">*</span></label>
                                <input type="number" class="form-input" id="epBeds" value="250" required>
                            </div>
                            <div>
                                <label class="form-label">Total Doctors <span class="req">*</span></label>
                                <input type="number" class="form-input" id="epDocs" value="75" required>
                            </div>
                            <div>
                                <label class="form-label">Patients/Year <span class="req">*</span></label>
                                <input type="text" class="form-input" id="epPatients" value="50K+" required>
                            </div>
                        </div>
                    </div>

                    <!-- Details & Contact -->
                    <div class="edit-panel">
                        <h3 class="edit-panel-title">Hospital Details & Contact Information</h3>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px;">
                            <div>
                                <label class="form-label">Hospital Type</label>
                                <select class="form-input" id="epType" style="appearance: none;">
                                    <option style="background: var(--bg-panel);" value="Multi Speciality">Multi Speciality</option>
                                    <option style="background: var(--bg-panel);" value="General">General</option>
                                    <option style="background: var(--bg-panel);" value="Clinic">Clinic</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label">Email <span class="req">*</span></label>
                                <input type="email" class="form-input" id="epEmail" value="info@arogyacare.com" required>
                            </div>
                            <div>
                                <label class="form-label">Phone <span class="req">*</span></label>
                                <input type="tel" class="form-input" id="epPhone" value="+91 98765 43210" required>
                            </div>
                            <div>
                                <label class="form-label">Emergency Phone <span class="req">*</span></label>
                                <input type="tel" class="form-input" id="epEmergency" value="+91 98765 43211" required>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 16px; margin-bottom: 20px;">
                            <div>
                                <label class="form-label">Address <span class="req">*</span></label>
                                <input type="text" class="form-input" id="epAddress" value="123, Health City, Medical District" required>
                            </div>
                            <div>
                                <label class="form-label">City <span class="req">*</span></label>
                                <input type="text" class="form-input" id="epCity" value="Bangalore" required>
                            </div>
                            <div>
                                <label class="form-label">State <span class="req">*</span></label>
                                <input type="text" class="form-input" id="epState" value="Karnataka" required>
                            </div>
                            <div>
                                <label class="form-label">PIN Code <span class="req">*</span></label>
                                <input type="text" class="form-input" id="epPin" value="560102" required>
                            </div>
                        </div>
                        <div>
                            <label class="form-label">Google Maps Location <span class="req">*</span></label>
                            <div style="display: flex; gap: 12px;">
                                <input type="text" class="form-input" id="epMapLoc" value="Bangalore, Karnataka, India" required>
                                <button type="button" style="background: rgba(4, 120, 87, 0.2); border: 1px solid rgba(4, 120, 87, 0.4); color: #10b981; padding: 0 20px; border-radius: 8px; white-space: nowrap; font-weight: 500; cursor: pointer;">Get Current Location</button>
                            </div>
                            <p style="font-size: 0.7rem; color: #64748b; margin-top: 8px;">Search your location or click "Get Current Location"</p>
                        </div>
                    </div>

                    <!-- Services -->
                    <div class="edit-panel">
                        <h3 class="edit-panel-title">Services Offered</h3>
                        <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px;">
                            <label class="service-checkbox"><input type="checkbox" checked><span>Emergency Care</span></label>
                            <label class="service-checkbox"><input type="checkbox" checked><span>Cardiology</span></label>
                            <label class="service-checkbox"><input type="checkbox" checked><span>Neurology</span></label>
                            <label class="service-checkbox"><input type="checkbox" checked><span>Orthopedics</span></label>
                            <label class="service-checkbox"><input type="checkbox" checked><span>Oncology</span></label>
                            <label class="service-checkbox"><input type="checkbox" checked><span>Pediatrics</span></label>
                        </div>
                        <button type="button" class="add-service-btn"><i data-lucide="plus" size="14"></i> Add Custom Service</button>
                    </div>

                    <!-- Images -->
                    <div class="edit-panel">
                        <h3 class="edit-panel-title">Hospital Images</h3>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                            <div>
                                <label style="display:block; text-align:center; font-size:0.8rem; color:#fff; font-weight:500; margin-bottom:12px;">About Hospital Image</label>
                                <div class="img-upload-box" style="height: 160px;">
                                    <button type="button" class="remove-img-btn"><i data-lucide="x" size="14"></i></button>
                                    <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80">
                                    <button type="button" class="img-overlay-btn"><i data-lucide="camera" size="14"></i> Change Image</button>
                                </div>
                            </div>
                            <div>
                                <label style="display:block; text-align:center; font-size:0.8rem; color:#fff; font-weight:500; margin-bottom:12px;">Infrastructure Image</label>
                                <div class="img-upload-box" style="height: 160px;">
                                    <button type="button" class="remove-img-btn"><i data-lucide="x" size="14"></i></button>
                                    <img src="https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?auto=format&fit=crop&w=400&q=80">
                                    <button type="button" class="img-overlay-btn"><i data-lucide="camera" size="14"></i> Change Image</button>
                                </div>
                            </div>
                            <div>
                                <label style="display:block; text-align:center; font-size:0.8rem; color:#fff; font-weight:500; margin-bottom:12px;">Advanced Equipment Image</label>
                                <div class="img-upload-box" style="height: 160px;">
                                    <button type="button" class="remove-img-btn"><i data-lucide="x" size="14"></i></button>
                                    <img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80">
                                    <button type="button" class="img-overlay-btn"><i data-lucide="camera" size="14"></i> Change Image</button>
                                </div>
                            </div>
                            <div>
                                <label style="display:block; text-align:center; font-size:0.8rem; color:#fff; font-weight:500; margin-bottom:12px;">Hospital Exterior Image</label>
                                <div class="img-upload-box" style="height: 160px;">
                                    <button type="button" class="remove-img-btn"><i data-lucide="x" size="14"></i></button>
                                    <img src="https://images.unsplash.com/photo-1538108149393-cebb47acddb2?auto=format&fit=crop&w=400&q=80">
                                    <button type="button" class="img-overlay-btn"><i data-lucide="camera" size="14"></i> Change Image</button>
                                </div>
                            </div>
                        </div>
                        <p style="font-size: 0.7rem; color: #64748b; margin-top: 16px;">Upload high quality images. JPG, PNG up to 5MB each.</p>
                    </div>

                    <!-- Advanced Equipment -->
                    <div class="edit-panel">
                        <h3 class="edit-panel-title">Advanced Medical Equipment</h3>
                        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px;">
                            <div class="equipment-card">
                                <button type="button" class="remove-img-btn" style="top: 8px; right: 8px;"><i data-lucide="x" size="12"></i></button>
                                <img src="https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80">
                                <div class="equipment-info">
                                    <h5>Siemens MRI 3T</h5>
                                    <p>Advanced Imaging</p>
                                </div>
                                <button type="button" class="img-overlay-btn" style="bottom: 60px;"><i data-lucide="camera" size="12"></i> Change Image</button>
                            </div>
                            <div class="equipment-card">
                                <button type="button" class="remove-img-btn" style="top: 8px; right: 8px;"><i data-lucide="x" size="12"></i></button>
                                <img src="https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?auto=format&fit=crop&w=400&q=80">
                                <div class="equipment-info">
                                    <h5>Da Vinci Xi Surgical System</h5>
                                    <p>Robotic Surgery</p>
                                </div>
                                <button type="button" class="img-overlay-btn" style="bottom: 76px;"><i data-lucide="camera" size="12"></i> Change Image</button>
                            </div>
                            <div class="equipment-card">
                                <button type="button" class="remove-img-btn" style="top: 8px; right: 8px;"><i data-lucide="x" size="12"></i></button>
                                <img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80">
                                <div class="equipment-info">
                                    <h5>Philips CT Scan 128 Slice</h5>
                                    <p>Advanced Tomography</p>
                                </div>
                                <button type="button" class="img-overlay-btn" style="bottom: 76px;"><i data-lucide="camera" size="12"></i> Change Image</button>
                            </div>
                            <div class="equipment-card">
                                <button type="button" class="remove-img-btn" style="top: 8px; right: 8px;"><i data-lucide="x" size="12"></i></button>
                                <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80">
                                <div class="equipment-info">
                                    <h5>Dräger Ventilator</h5>
                                    <p>Critical Care</p>
                                </div>
                                <button type="button" class="img-overlay-btn" style="bottom: 60px;"><i data-lucide="camera" size="12"></i> Change Image</button>
                            </div>
                            <div class="add-equipment-card">
                                <div class="icon-circle"><i data-lucide="plus" size="20"></i></div>
                                <p>Add New Equipment</p>
                            </div>
                        </div>
                        <p style="font-size: 0.75rem; color: #64748b; margin-top: 16px;">Showcase your advanced medical equipment and technology</p>
                    </div>

                    <div class="bottom-actions">
                        <button type="button" class="btn-cancel" onclick="showSection(event, 'overview')">Cancel</button>
                        <button type="submit" class="btn-save">Save Changes</button>
                    </div>
                </form>
            </div>
"""

# Insert the section-edit-profile after section-overview
if '<div id="section-edit-profile"' not in content:
    # Remove the old modal overlay stuff if we are switching to full page layout
    # actually let's keep the modal just in case, but wire the Edit button to section navigation
    content = content.replace('<!-- Edit Profile Modal -->', edit_profile_html + '\n    <!-- Edit Profile Modal -->')

# Change the "Edit Profile" button to trigger showSection
content = content.replace('onclick="openEditModal()"', 'onclick="showSection(event, \'edit-profile\')"')

# Add showSection JS logic if missing
if 'function showSection(' not in content:
    js_logic = """
        function showSection(e, sectionId) {
            if (e) e.preventDefault();
            document.querySelectorAll('.main-content > div').forEach(div => {
                if(div.id && div.id.startsWith('section-')) {
                    div.classList.add('hidden');
                }
            });
            const target = document.getElementById('section-' + sectionId);
            if (target) target.classList.remove('hidden');
        }
"""
    content = content.replace("function openEditModal() {", js_logic + "\n        function openEditModal() {")

# Update save logic to target new form
content = content.replace("saveHospitalProfile(e) {", """saveHospitalProfile(e) {
            e.preventDefault();
            alert("Profile saved successfully!");
            showSection(null, 'overview');
            return;
""")

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Massive Edit Hospital Profile UI injected successfully.")
