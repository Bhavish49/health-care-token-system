import re

admin_path = r"c:\healthCareTokenSystem\dashboards\admin.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Leaflet CSS/JS to <head>
if "unpkg.com/leaflet" not in content:
    leaflet_tags = """    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://unpkg.com/@supabase/supabase-js@2"></script>
    <!-- Leaflet Map -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>"""
    content = content.replace("    <script src=\"https://unpkg.com/lucide@latest\"></script>\n    <script src=\"https://unpkg.com/@supabase/supabase-js@2\"></script>", leaflet_tags)

# 2. Add styles for the premium modal
premium_styles = """
        /* Premium Edit Modal */
        .modal-content.premium { max-width: 900px; display: grid; grid-template-columns: 320px 1fr; padding: 0; overflow: hidden; }
        .modal-aside { background: linear-gradient(135deg, rgba(14, 165, 233, 0.05), rgba(15, 23, 42, 1)); padding: 40px 32px; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 24px; }
        .modal-body { padding: 40px 32px; overflow-y: auto; max-height: 85vh; }
        
        .photo-dropzone { background: rgba(10, 15, 28, 0.6); border: 2px dashed rgba(255,255,255,0.15); border-radius: 20px; aspect-ratio: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; cursor: pointer; transition: 0.2s; position: relative; overflow: hidden; margin-bottom: 16px; }
        .photo-dropzone:hover { border-color: var(--primary); background: rgba(14, 165, 233, 0.05); }
        .photo-dropzone img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: none; }
        
        #mapPicker { width: 100%; height: 200px; border-radius: 12px; margin-bottom: 16px; border: 1px solid var(--border-color); background-color: var(--bg-dark); }
        .search-results { position: absolute; top: 100%; left: 0; right: 0; background: var(--bg-panel); border: 1px solid var(--border-color); border-radius: 12px; max-height: 200px; overflow-y: auto; z-index: 1000; margin-top: 4px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .search-item { padding: 12px 16px; cursor: pointer; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: #cbd5e1; }
        .search-item:hover { background: rgba(14, 165, 233, 0.1); color: #fff; }
        .confirmed-address { background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #fff; display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start; }
"""
content = content.replace("/* Modal Overlay for Edit Profile */", premium_styles + "\n        /* Modal Overlay for Edit Profile */")

# 3. Replace the simple modal HTML with premium modal HTML
simple_modal_pattern = r'<!-- Edit Profile Modal -->.*?<script src="\.\./js/services/supabase\.js">'

premium_modal_html = """<!-- Edit Profile Modal -->
    <div class="modal-overlay" id="editModal">
        <div class="modal-content premium">
            <div class="modal-aside">
                <div>
                    <h2 style="font-family: 'Outfit'; font-size: 1.5rem; margin-bottom: 8px;">Facility Identity</h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Upload a high-quality exterior photo to help patients recognize your facility immediately.</p>
                </div>
                
                <div class="photo-dropzone" onclick="document.getElementById('fileInput').click()">
                    <i data-lucide="image-plus" style="color: var(--primary); width: 32px; height: 32px;" id="dzIcon"></i>
                    <span style="font-size: 0.8rem; font-weight: 600; color: #fff;" id="dzText">Click to upload photo</span>
                    <img id="photoPreview" alt="Facility Preview">
                    <input type="file" id="fileInput" hidden accept="image/*" onchange="handleFilePreview(event)">
                </div>

                <div class="form-group" style="margin-bottom: 0;">
                    <label>Hospital Name</label>
                    <input type="text" id="editHospName" required placeholder="e.g. Apollo Hospital">
                </div>
            </div>

            <div class="modal-body">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <h3 style="font-family: 'Outfit'; margin: 0;">Location & Details</h3>
                    <button class="close-btn" onclick="closeEditModal()"><i data-lucide="x"></i></button>
                </div>

                <div class="form-group" style="position: relative;">
                    <label>Facility Address (Free Search)</label>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="searchAddressInput" placeholder="Search for hospital name or area..." oninput="handleAddressSearch(this.value)">
                        <button type="button" onclick="toggleMap()" style="background: rgba(14, 165, 233, 0.1); border: 1px solid var(--primary); color: var(--primary); border-radius: 12px; padding: 0 16px; cursor: pointer;"><i data-lucide="map"></i></button>
                    </div>
                    <div id="searchResults" class="search-results hidden"></div>
                </div>

                <div id="mapPicker" class="hidden"></div>
                <div id="confirmedAddressCard" class="confirmed-address hidden">
                    <i data-lucide="check-circle" style="color: var(--success); margin-top: 2px;"></i>
                    <div id="confirmedAddressText">No address selected</div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label>Primary Specialty</label>
                        <select id="editHospSpec" style="width: 100%; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; color: #fff; padding: 14px 16px; font-family: inherit; font-size: 0.95rem;">
                            <option style="background: #111827;" value="General Medicine">General Medicine</option>
                            <option style="background: #111827;" value="Cardiology">Cardiology</option>
                            <option style="background: #111827;" value="Orthopedics">Orthopedics</option>
                            <option style="background: #111827;" value="Neurology">Neurology</option>
                            <option style="background: #111827;" value="Pediatrics">Pediatrics</option>
                            <option style="background: #111827;" value="Multi-Speciality">Multi-Speciality</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Total Doctors</label>
                        <input type="number" id="editHospDocs" min="0" placeholder="e.g. 50">
                    </div>
                </div>

                <div class="form-group">
                    <label>Why Choose Our Facility?</label>
                    <textarea id="editHospDesc" rows="4" placeholder="Highlight your top-tier equipment, patient care standards, and awards..." required></textarea>
                </div>

                <button class="btn-edit" onclick="saveHospitalProfile(event)" style="width: 100%; justify-content: center; padding: 16px; margin-top: 10px; font-size: 1rem;">Save Profile & Setup Facility</button>
            </div>
        </div>
    </div>

    <script src="../js/services/supabase.js">"""

content = re.sub(simple_modal_pattern, premium_modal_html, content, flags=re.DOTALL)

# 4. Add the map and image logic to JS
js_logic = """
        // JS additions for premium modal
        let map, marker;
        let searchTimeout;
        let isMapVisible = false;
        let base64Photo = null;
        let selectedAddress = null;

        function handleFilePreview(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.getElementById('photoPreview');
                preview.src = e.target.result;
                preview.style.display = 'block';
                document.getElementById('dzIcon').style.display = 'none';
                document.getElementById('dzText').style.display = 'none';
                base64Photo = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        function toggleMap() {
            const mapDiv = document.getElementById('mapPicker');
            isMapVisible = !isMapVisible;
            if (isMapVisible) {
                mapDiv.classList.remove('hidden');
                if (!map) initLeafletMap();
                else setTimeout(() => map.invalidateSize(), 100);
            } else {
                mapDiv.classList.add('hidden');
            }
        }

        function initLeafletMap() {
            map = L.map('mapPicker').setView([20.5937, 78.9629], 5);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO'
            }).addTo(map);

            marker = L.marker([20.5937, 78.9629], {draggable: true}).addTo(map);

            marker.on('dragend', function(e) {
                const pos = marker.getLatLng();
                reverseGeocode(pos.lat, pos.lng);
            });

            map.on('click', function(e) {
                marker.setLatLng(e.latlng);
                reverseGeocode(e.latlng.lat, e.latlng.lng);
            });
        }

        async function reverseGeocode(lat, lon) {
            try {
                const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                const data = await res.json();
                if (data.display_name) confirmAddress(data.display_name, lat, lon);
            } catch (err) { console.error(err); }
        }

        function handleAddressSearch(query) {
            clearTimeout(searchTimeout);
            const resultsDiv = document.getElementById('searchResults');
            
            if (query.length < 3) {
                resultsDiv.classList.add('hidden');
                return;
            }

            searchTimeout = setTimeout(async () => {
                try {
                    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&addressdetails=1`);
                    const results = await res.json();
                    
                    resultsDiv.innerHTML = '';
                    if (results.length > 0) {
                        resultsDiv.classList.remove('hidden');
                        results.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'search-item';
                            
                            let displayText = item.display_name;
                            if (item.name && item.name !== "" && !item.display_name.startsWith(item.name)) {
                                displayText = `<b>${item.name}</b>, ${item.display_name}`;
                            } else if (item.name && item.name !== "") {
                                displayText = item.display_name.replace(item.name, `<b>${item.name}</b>`);
                            }
                            
                            div.innerHTML = `<i data-lucide="map-pin" size="14" style="color: var(--primary)"></i> <span>${displayText}</span>`;
                            div.onclick = () => {
                                confirmAddress(item.display_name, item.lat, item.lon);
                                resultsDiv.classList.add('hidden');
                                document.getElementById('searchAddressInput').value = '';
                                if (!map) {
                                    toggleMap();
                                }
                                map.setView([item.lat, item.lon], 16);
                                marker.setLatLng([item.lat, item.lon]);
                            };
                            resultsDiv.appendChild(div);
                        });
                        lucide.createIcons();
                    } else {
                        resultsDiv.classList.add('hidden');
                    }
                } catch (err) { console.error(err); }
            }, 500);
        }

        function confirmAddress(addrString, lat, lon) {
            selectedAddress = addrString;
            const card = document.getElementById('confirmedAddressCard');
            card.classList.remove('hidden');
            document.getElementById('confirmedAddressText').innerHTML = `<b>Selected Address:</b><br>${addrString}`;
        }
        
        // Add map visibility logic
"""
content = content.replace("        let currentHosp = null;", "        let currentHosp = null;\n" + js_logic)

# 5. Fix form loading in loadDashboard()
old_loading_logic = """                // Pre-fill edit modal
                document.getElementById('editHospName').value = hospital.name || '';
                document.getElementById('editHospAddr').value = hospital.address || '';
                document.getElementById('editHospPhoto').value = hospital.photo_url || '';
                document.getElementById('editHospSpec').value = hospital.specialty || '';
                document.getElementById('editHospDocs').value = hospital.staff_count || '';
                document.getElementById('editHospDesc').value = hospital.description || '';"""

new_loading_logic = """                // Pre-fill edit modal
                document.getElementById('editHospName').value = hospital.name || '';
                
                if (hospital.address) {
                    confirmAddress(hospital.address, 20, 78);
                }
                
                if (hospital.photo_url) {
                    const preview = document.getElementById('photoPreview');
                    preview.src = hospital.photo_url;
                    preview.style.display = 'block';
                    document.getElementById('dzIcon').style.display = 'none';
                    document.getElementById('dzText').style.display = 'none';
                    base64Photo = hospital.photo_url;
                }
                
                document.getElementById('editHospSpec').value = hospital.specialty || 'General Medicine';
                document.getElementById('editHospDocs').value = hospital.staff_count || '';
                document.getElementById('editHospDesc').value = hospital.description || '';"""

content = content.replace(old_loading_logic, new_loading_logic)

# 6. Fix saving logic in saveHospitalProfile()
old_save_logic = """            const updates = {
                name: document.getElementById('editHospName').value,
                address: document.getElementById('editHospAddr').value,
                photo_url: document.getElementById('editHospPhoto').value || null,
                specialty: document.getElementById('editHospSpec').value,
                staff_count: parseInt(document.getElementById('editHospDocs').value) || 0,
                description: document.getElementById('editHospDesc').value,
                onboarding_complete: true
            };"""

new_save_logic = """            const updates = {
                name: document.getElementById('editHospName').value,
                address: selectedAddress || currentHosp.address,
                photo_url: base64Photo || currentHosp.photo_url,
                specialty: document.getElementById('editHospSpec').value,
                staff_count: parseInt(document.getElementById('editHospDocs').value) || 0,
                description: document.getElementById('editHospDesc').value,
                onboarding_complete: true
            };"""

content = content.replace(old_save_logic, new_save_logic)

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Premium modal re-integrated successfully!")
