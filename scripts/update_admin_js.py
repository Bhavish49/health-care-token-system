import re

admin_path = r"c:\healthCareTokenSystem\dashboards\admin.html"

with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Javascript bindings
old_load_dashboard = """
            if (hospital) {
                currentHosp = hospital;
                document.getElementById('hospitalTitle').innerText = hospital.name;
                document.getElementById('hospitalSub').innerText = hospital.address || 'Configure your facility location to start accepting patients.';
                document.getElementById('hospLocStat').innerText = hospital.address || 'Not Set';
                document.getElementById('statDocCount').innerText = hospital.staff_count || 0;
                document.getElementById('hospSpecialty').innerText = hospital.specialty || 'General Medicine';
                document.getElementById('hospBio').innerText = hospital.description || 'Facility bio not yet configured.';
                
                if (hospital.photo_url) {
                    const preview = document.getElementById('photoPreview');
                    preview.src = hospital.photo_url;
                    preview.style.display = 'block';
                    document.getElementById('dzPlaceholder').classList.add('hidden');
                    base64Photo = hospital.photo_url;
                }
                document.getElementById('editLoc').value = hospital.address || '';
                document.getElementById('editSpec').value = hospital.specialty || 'General Medicine';
                document.getElementById('editDocCount').value = hospital.staff_count || '';
                document.getElementById('editDesc').value = hospital.description || '';

                if (hospital.onboarding_complete === false) {
                    document.getElementById('onboardingBanner').classList.remove('hidden');
                    document.getElementById('cancelBtn').classList.add('hidden');
                    openEditModal();
                }
                loadDoctors(hospital.id);
            } else {"""

new_load_dashboard = """
            if (hospital) {
                currentHosp = hospital;
                
                // Update new UI bindings
                document.getElementById('hospitalTitle').innerText = hospital.name || 'Hospital Name';
                
                if (document.getElementById('hospBio')) {
                    document.getElementById('hospBio').innerText = hospital.description || 'Providing world-class healthcare services with state-of-the-art technology.';
                }
                if (document.getElementById('hospLocStat')) {
                    document.getElementById('hospLocStat').innerText = hospital.address || 'Location Not Set';
                }
                if (document.getElementById('statDocCount')) {
                    document.getElementById('statDocCount').innerText = hospital.staff_count || 0;
                }
                if (document.getElementById('statDocs')) {
                    document.getElementById('statDocs').innerText = (hospital.staff_count || 0) + "+";
                }
                
                if (hospital.photo_url) {
                    const heroImg = document.getElementById('heroBannerImg');
                    if (heroImg) heroImg.style.backgroundImage = `url('${hospital.photo_url}')`;
                    
                    const preview = document.getElementById('photoPreview');
                    if (preview) {
                        preview.src = hospital.photo_url;
                        preview.style.display = 'block';
                        const placeholder = document.getElementById('dzPlaceholder');
                        if (placeholder) placeholder.classList.add('hidden');
                    }
                    base64Photo = hospital.photo_url;
                }
                
                // Form bindings
                if (document.getElementById('editLoc')) document.getElementById('editLoc').value = hospital.address || '';
                if (document.getElementById('editSpec')) document.getElementById('editSpec').value = hospital.specialty || 'General Medicine';
                if (document.getElementById('editDocCount')) document.getElementById('editDocCount').value = hospital.staff_count || '';
                if (document.getElementById('editDesc')) document.getElementById('editDesc').value = hospital.description || '';

                if (hospital.onboarding_complete === false) {
                    const banner = document.getElementById('onboardingBanner');
                    if (banner) banner.classList.remove('hidden');
                    const cancelBtn = document.getElementById('cancelBtn');
                    if (cancelBtn) cancelBtn.classList.add('hidden');
                    openEditModal();
                }
                loadDoctors(hospital.id);
            } else {"""

content = content.replace(old_load_dashboard, new_load_dashboard)

# Fix search logic to prioritize name
search_logic_old = """
            results.forEach(item => {
                const div = document.createElement('div');
                div.className = 'search-item';
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                div.style.gap = '10px';
                div.innerHTML = `<i data-lucide="map-pin" size="14" style="color: var(--primary)"></i> <span>${item.display_name}</span>`;
"""

search_logic_new = """
            results.forEach(item => {
                const div = document.createElement('div');
                div.className = 'search-item';
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                div.style.gap = '10px';
                
                // If it's a named place (like a hospital), show its name followed by the address
                let displayText = item.display_name;
                if (item.name && item.name !== "" && !item.display_name.startsWith(item.name)) {
                    displayText = `<b>${item.name}</b>, ${item.display_name}`;
                } else if (item.name && item.name !== "") {
                    displayText = item.display_name.replace(item.name, `<b>${item.name}</b>`);
                }
                
                div.innerHTML = `<i data-lucide="map-pin" size="14" style="color: #0ea5e9"></i> <span>${displayText}</span>`;
"""

content = content.replace(search_logic_old, search_logic_new)

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("JS bindings and search logic updated successfully.")
