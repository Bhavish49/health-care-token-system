import re

admin_path = r"c:\healthCareTokenSystem\dashboards\admin.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_styles = """
        body { background-color: #0b1120; color: #cbd5e1; font-family: 'Inter', sans-serif; }
        .dashboard-layout { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
        .sidebar { background: #0f172a; border-right: 1px solid rgba(255,255,255,0.05); padding: 24px 16px; display: flex; flex-direction: column; gap: 4px; }
        .sidebar .brand { padding: 0 16px 24px; font-family: 'Outfit', sans-serif; font-size: 1.25rem; color: #fff; display: flex; align-items: center; gap: 12px; font-weight: 700; }
        .nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 16px; color: #94a3b8; text-decoration: none; border-radius: 8px; font-size: 0.85rem; font-weight: 500; transition: all 0.2s; }
        .nav-item:hover, .nav-item.active { background: rgba(14, 165, 233, 0.1); color: #0ea5e9; }
        .nav-item i { width: 18px; height: 18px; }
        
        .main-content { padding: 32px 40px; overflow-y: auto; background: #0b1120; }
        .header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
        .header-top h1 { font-size: 1.5rem; color: #fff; font-family: 'Outfit'; margin-bottom: 4px; }
        .header-top p { font-size: 0.85rem; color: #64748b; margin: 0; }
        
        .hero-banner-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .hero-img { background: url('https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80') center/cover; border-radius: 16px; min-height: 280px; position: relative; }
        .hero-img::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgba(15,23,42,0.8), transparent); border-radius: 16px; }
        .hero-info { background: #1e293b; border-radius: 16px; padding: 32px; border: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; justify-content: space-between; }
        .hero-info h2 { font-size: 1.6rem; color: #fff; font-family: 'Outfit'; margin-bottom: 8px; }
        .hero-info p { font-size: 0.9rem; color: #94a3b8; line-height: 1.6; margin-bottom: 24px; }
        .info-stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 16px; }
        .info-stat-item p { margin: 0; font-size: 0.75rem; color: #64748b; }
        .info-stat-item h4 { margin: 0; font-size: 1.1rem; color: #fff; font-family: 'Outfit'; }
        
        .metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: #1e293b; border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 16px; }
        .metric-icon { width: 48px; height: 48px; border-radius: 12px; background: rgba(14, 165, 233, 0.1); color: #0ea5e9; display: flex; align-items: center; justify-content: center; }
        .metric-card h3 { font-size: 1.25rem; color: #fff; margin-bottom: 4px; font-family: 'Outfit'; margin-top: 0; }
        .metric-card p { font-size: 0.8rem; margin: 0; color: #94a3b8; }
        
        .content-row { display: grid; grid-template-columns: 1fr 1.2fr; gap: 20px; margin-bottom: 20px; }
        .panel { background: #1e293b; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); padding: 24px; }
        .panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .panel-header h3 { font-size: 1.1rem; color: #fff; font-family: 'Outfit'; margin: 0; }
        .panel-header a { font-size: 0.8rem; color: #0ea5e9; text-decoration: none; }
        
        .services-list { display: grid; grid-template-columns: 1fr; gap: 16px; }
        .service-item { display: flex; align-items: flex-start; gap: 16px; }
        .service-icon { width: 32px; height: 32px; border-radius: 50%; background: rgba(239, 68, 68, 0.1); color: #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .service-info h4 { margin: 0 0 4px 0; font-size: 0.9rem; color: #fff; }
        .service-info p { margin: 0; font-size: 0.8rem; color: #64748b; }
        
        .checklist { list-style: none; padding: 0; margin: 20px 0; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .checklist li { font-size: 0.85rem; color: #cbd5e1; display: flex; align-items: center; gap: 8px; }
        .checklist li i { color: #22c55e; width: 16px; height: 16px; }
        
        .loc-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }
        .loc-card { background: rgba(15, 23, 42, 0.5); border-radius: 12px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); display: flex; gap: 12px; align-items: flex-start; }
        
        .img-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        .img-card { border-radius: 12px; overflow: hidden; background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.05); }
        .img-card img { width: 100%; height: 120px; object-fit: cover; }
        .img-card div { padding: 12px; }
        .img-card h5 { margin: 0 0 4px 0; font-size: 0.85rem; color: #fff; }
        .img-card p { margin: 0; font-size: 0.75rem; color: #64748b; }

        /* Existing Modal/Form/Doctor Grid classes */
        .modal-overlay { position: fixed; inset: 0; background: rgba(2, 6, 23, 0.85); backdrop-filter: blur(16px); display: none; align-items: center; justify-content: center; z-index: 5000; padding: 20px; animation: fadeIn 0.3s ease-out; }
        .modal-overlay.open { display: flex; }
        .modal-content { background: #0f172a; width: 100%; max-width: 850px; max-height: 90vh; overflow: hidden; border-radius: 32px; border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 50px 100px -20px rgba(0,0,0,0.8); display: grid; grid-template-columns: 300px 1fr; }
        .modal-aside { background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, transparent 100%); padding: 40px; border-right: 1px solid rgba(255, 255, 255, 0.05); display: flex; flex-direction: column; gap: 24px; }
        .modal-body { padding: 40px; overflow-y: auto; }
        .photo-dropzone { width: 100%; aspect-ratio: 16/9; background: rgba(30, 41, 59, 0.5); border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden; margin-bottom: 24px; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; font-size: 0.75rem; font-weight: 700; color: #64748b; margin-bottom: 8px; text-transform: uppercase; }
        .input-group input, .input-group select, .input-group textarea { width: 100%; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; color: #fff; padding: 14px 16px; font-family: inherit; font-size: 0.95rem; transition: all 0.2s; }
        .input-group select option { background-color: #1e293b; color: #fff; padding: 10px; }
        .btn-primary { background: #f97316; color: #ffffff; padding: 10px 22px; border-radius: 8px; font-weight: 700; border: none; cursor: pointer; }
        .hidden { display: none !important; }
        #mapPicker { z-index: 5; }
        .leaflet-container { background: #0f172a !important; }
        .search-results { position: absolute; top: 100%; left: 0; right: 0; background: #1e293b; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; z-index: 1000; max-height: 200px; overflow-y: auto; margin-top: 4px; }
        .search-item { padding: 12px 16px; cursor: pointer; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; color: #cbd5e1; }
        .search-item:hover { background: rgba(14, 165, 233, 0.1); color: #fff; }
        .doctor-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
        .doctor-admin-card { background: rgba(30, 41, 59, 0.5); padding: 24px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.05); display: flex; align-items: center; gap: 16px; transition: all 0.2s; }
"""

new_body = """    <div class="dashboard-layout">
        <aside class="sidebar">
            <div class="brand">
                <i data-lucide="shield-plus" style="color: #0ea5e9;"></i> MediQ Care
            </div>
            <nav style="flex: 1; display: flex; flex-direction: column; gap: 4px;">
                <a href="#" class="nav-item active" onclick="showSection(event, 'overview')"><i data-lucide="layout-dashboard"></i> Hospital Profile</a>
                <a href="#" class="nav-item" onclick="showSection(event, 'doctors')"><i data-lucide="users"></i> Doctors</a>
                <a href="#" class="nav-item" onclick="openEditModal(event)"><i data-lucide="building-2"></i> Edit Facility</a>
                <a href="#" class="nav-item"><i data-lucide="layers"></i> Departments</a>
                <a href="#" class="nav-item"><i data-lucide="stethoscope"></i> Services</a>
                <a href="#" class="nav-item"><i data-lucide="bed"></i> Facilities</a>
                <a href="#" class="nav-item"><i data-lucide="building"></i> Infrastructure</a>
                <a href="#" class="nav-item"><i data-lucide="image"></i> Gallery</a>
                <a href="#" class="nav-item"><i data-lucide="map-pin"></i> Location</a>
                <a href="#" class="nav-item"><i data-lucide="award"></i> Achievements</a>
                <a href="#" class="nav-item"><i data-lucide="users-round"></i> Patients</a>
                <a href="#" class="nav-item"><i data-lucide="file-text"></i> Reports</a>
                <a href="#" class="nav-item"><i data-lucide="settings"></i> Settings</a>
            </nav>
            <a href="#" onclick="handleLogout()" class="nav-item" style="color: #ef4444;"><i data-lucide="log-out"></i> Logout</a>
        </aside>

        <main class="main-content">
            <div id="section-overview">
                <div class="header-top">
                    <div>
                        <h1>Hospital Profile</h1>
                        <p>Manage your hospital information and showcase your services</p>
                    </div>
                    <div style="text-align: right; display: flex; align-items: center; gap: 12px;">
                        <div style="text-align: right;">
                            <p style="margin: 0; color: #fff; font-weight: 600; font-size: 0.9rem;">Admin</p>
                            <p style="margin: 0; font-size: 0.75rem; color: #64748b;">Super Admin</p>
                        </div>
                        <div style="width: 40px; height: 40px; background: #f97316; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff;"><i data-lucide="building"></i></div>
                    </div>
                </div>

                <div class="hero-banner-row">
                    <div class="hero-img" id="heroBannerImg"></div>
                    <div class="hero-info">
                        <div>
                            <div style="display: inline-flex; align-items: center; gap: 6px; color: #22c55e; font-size: 0.75rem; font-weight: 600; margin-bottom: 12px; background: rgba(34, 197, 94, 0.1); padding: 4px 10px; border-radius: 100px;">
                                <i data-lucide="check-circle" size="14"></i> Verified Hospital
                            </div>
                            <h2 id="hospitalTitle">Loading...</h2>
                            <p id="hospBio">Providing world-class healthcare services with state-of-the-art technology and a team of highly experienced medical professionals.</p>
                        </div>
                        <div class="info-stats-grid">
                            <div class="info-stat-item"><p>Established</p><h4 id="statEst">2010</h4></div>
                            <div class="info-stat-item"><p>Total Beds</p><h4 id="statBeds">250+</h4></div>
                            <div class="info-stat-item"><p>Total Doctors</p><h4 id="statDocCount">0</h4></div>
                            <div class="info-stat-item"><p>Patients/Year</p><h4 id="statPat">50K+</h4></div>
                        </div>
                    </div>
                </div>

                <div class="metrics-row">
                    <div class="metric-card">
                        <div class="metric-icon" style="color: #eab308; background: rgba(234, 179, 8, 0.1);"><i data-lucide="building"></i></div>
                        <div><h3 id="statDepts">25+</h3><p>Specialized Departments</p></div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon" style="color: #0ea5e9; background: rgba(14, 165, 233, 0.1);"><i data-lucide="user"></i></div>
                        <div><h3 id="statDocs">75+</h3><p>Experienced Doctors</p></div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon" style="color: #22c55e; background: rgba(34, 197, 94, 0.1);"><i data-lucide="bed"></i></div>
                        <div><h3 id="statBeds2">250+</h3><p>Advanced Beds</p></div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon" style="color: #f97316; background: rgba(249, 115, 22, 0.1);"><i data-lucide="users"></i></div>
                        <div><h3 id="statPatients">50K+</h3><p>Patients Treated/Year</p></div>
                    </div>
                </div>

                <div class="content-row">
                    <div class="panel">
                        <div class="panel-header">
                            <h3>Our Services</h3>
                            <a href="#">View All</a>
                        </div>
                        <div class="services-list">
                            <div class="service-item">
                                <div class="service-icon"><i data-lucide="activity"></i></div>
                                <div class="service-info"><h4>Emergency Care</h4><p>24/7 Emergency and Trauma Services</p></div>
                            </div>
                            <div class="service-item">
                                <div class="service-icon" style="color: #eab308; background: rgba(234,179,8,0.1);"><i data-lucide="heart"></i></div>
                                <div class="service-info"><h4>Cardiology</h4><p>Advanced heart care and interventions</p></div>
                            </div>
                            <div class="service-item">
                                <div class="service-icon" style="color: #0ea5e9; background: rgba(14,165,233,0.1);"><i data-lucide="brain"></i></div>
                                <div class="service-info"><h4>Neurology</h4><p>Brain and nervous system specialists</p></div>
                            </div>
                            <div class="service-item">
                                <div class="service-icon" style="color: #8b5cf6; background: rgba(139,92,246,0.1);"><i data-lucide="bone"></i></div>
                                <div class="service-info"><h4>Orthopedics</h4><p>Bone, joint and spine care</p></div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel">
                        <div class="panel-header">
                            <h3>About Our Hospital</h3>
                        </div>
                        <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">Our facility is a NABH accredited, multi-speciality hospital equipped with cutting-edge medical technology. We focus on patient-centric care.</p>
                        
                        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px;">
                            <ul class="checklist">
                                <li><i data-lucide="check-circle"></i> 24/7 Emergency Services</li>
                                <li><i data-lucide="check-circle"></i> Advanced ICUs</li>
                                <li><i data-lucide="check-circle"></i> Int. Standard Infrastructure</li>
                                <li><i data-lucide="check-circle"></i> Highly Qualified Team</li>
                                <li><i data-lucide="check-circle"></i> Cashless Insurance</li>
                                <li><i data-lucide="check-circle"></i> Patient-centric Approach</li>
                            </ul>
                            <div>
                                <img src="https://images.unsplash.com/photo-1538108149393-cebb47acddb2?auto=format&fit=crop&w=400&q=80" style="width: 100%; height: 120px; object-fit: cover; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                            </div>
                        </div>
                        
                        <div class="loc-cards">
                            <div class="loc-card">
                                <i data-lucide="map-pin" style="color: #0ea5e9; margin-top: 4px;"></i>
                                <div>
                                    <h5 style="margin:0 0 4px 0; color:#fff; font-size:0.85rem;">Hospital Address</h5>
                                    <p id="hospLocStat" style="margin:0; font-size:0.75rem; color:#64748b;">Not Set</p>
                                </div>
                            </div>
                            <div class="loc-card">
                                <i data-lucide="crosshair" style="color: #22c55e; margin-top: 4px;"></i>
                                <div>
                                    <h5 style="margin:0 0 4px 0; color:#fff; font-size:0.85rem;">Current Location</h5>
                                    <p style="margin:0; font-size:0.75rem; color:#64748b;">Verified <br> Accuracy: High</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="panel">
                    <div class="panel-header">
                        <h3>Advanced Medical Equipment</h3>
                        <a href="#">View All</a>
                    </div>
                    <div class="img-grid">
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80"><div><h5>Siemens MRI 3T</h5><p>Advanced Imaging</p></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?auto=format&fit=crop&w=400&q=80"><div><h5>Da Vinci Surgical System</h5><p>Robotic Surgery</p></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80"><div><h5>Philips CT Scan</h5><p>Advanced Tomography</p></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80"><div><h5>Dräger Ventilator</h5><p>Critical Care</p></div></div>
                    </div>
                </div>

                <div class="panel" style="margin-top: 20px;">
                    <div class="panel-header">
                        <h3>Hospital Gallery</h3>
                        <a href="#">View All</a>
                    </div>
                    <div class="img-grid">
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80"><div><h5>Reception</h5></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?auto=format&fit=crop&w=400&q=80"><div><h5>Operation Theatre</h5></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1538108149393-cebb47acddb2?auto=format&fit=crop&w=400&q=80"><div><h5>Patient Ward</h5></div></div>
                        <div class="img-card"><img src="https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80"><div><h5>Laboratory</h5></div></div>
                    </div>
                </div>
            </div>

            <div id="section-doctors" class="hidden">
                <header style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
                    <h2 style="font-size: 2rem; margin: 0; color: #fff; font-family: 'Outfit';">Staff Directory</h2>
                    <button class="btn-primary" onclick="promptInvite()">Invite Doctor</button>
                </header>
                <div class="doctor-grid" id="doctorGrid"></div>
            </div>
        </main>
    </div>"""

# Replace styles
content = re.sub(r'<style>.*?</style>', '<style>\n' + new_styles + '\n    </style>', content, flags=re.DOTALL)
# Replace layout
content = re.sub(r'<div class="dashboard-layout">.*?<!-- MOBILE BOTTOM NAV -->', new_body + '\n\n    <!-- MOBILE BOTTOM NAV -->', content, flags=re.DOTALL)

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Python script executed successfully.")
