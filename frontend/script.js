// Agadh Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

// Global variables
let currentUser = null;
let currentLanguage = 'en';
let services = [];
let employees = [];

// Initialize application
function initApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadServices();
    loadEmployees();
    
    // Check for saved user session
    checkUserSession();
    
    // Initialize chatbot
    initChatbot();
}

// Set up event listeners
function setupEventListeners() {
    // Language toggle
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setLanguage(this.dataset.lang);
        });
    });
    
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
            
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Mobile menu toggle
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const navMenu = document.querySelector('.nav-menu');
            navMenu.classList.toggle('active');
        });
    }
    
    // Login/Register buttons
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', showLoginModal);
    }
    
    if (registerBtn) {
        registerBtn.addEventListener('click', showRegisterModal);
    }
    
    // Modal close buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', closeAllModals);
    });
    
    // Modal background close
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAllModals();
            }
        });
    });
    
    // Switch between login/register modals
    const switchToRegister = document.getElementById('switchToRegister');
    const switchToLogin = document.getElementById('switchToLogin');
    
    if (switchToRegister) {
        switchToRegister.addEventListener('click', function(e) {
            e.preventDefault();
            closeAllModals();
            showRegisterModal();
        });
    }
    
    if (switchToLogin) {
        switchToLogin.addEventListener('click', function(e) {
            e.preventDefault();
            closeAllModals();
            showLoginModal();
        });
    }
    
    // Forms
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Explore services button
    const exploreServicesBtn = document.getElementById('exploreServices');
    if (exploreServicesBtn) {
        exploreServicesBtn.addEventListener('click', function() {
            scrollToSection('services');
        });
    }
    
    // Chat now button
    const chatNowBtn = document.getElementById('chatNow');
    if (chatNowBtn) {
        chatNowBtn.addEventListener('click', function() {
            toggleChatbot();
        });
    }
    
    // View all services
    const viewAllBtn = document.getElementById('viewAllServices');
    if (viewAllBtn) {
        viewAllBtn.addEventListener('click', function() {
            // In a real app, this would navigate to services page
            scrollToSection('services');
        });
    }
}

// Language handling
function setLanguage(lang) {
    currentLanguage = lang;
    
    // Update active language button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.lang === lang) {
            btn.classList.add('active');
        }
    });
    
    // Update content based on language
    updateContentForLanguage(lang);
    
    // Save language preference
    localStorage.setItem('agadh_language', lang);
}

function updateContentForLanguage(lang) {
    // This would update all text content based on language
    // For now, we'll just update a few example elements
    
    const translations = {
        en: {
            welcome: "Welcome to Agadh",
            subtitle: "Kerala's Digital Service Center",
            description: "One-stop platform for all government services through Akshaya Centers. Apply for certificates, documents, and services online with ease.",
            explore: "Explore Services",
            chat: "Chat with Assistant"
        },
        ml: {
            welcome: "അഗാധിലേക്ക് സ്വാഗതം",
            subtitle: "കേരളത്തിന്റെ ഡിജിറ്റൽ സർവീസ് സെന്റർ",
            description: "അക്ഷയ സെന്ററുകൾ വഴി എല്ലാ സർക്കാർ സേവനങ്ങൾക്കുമുള്ള വൺ-സ്റ്റോപ്പ് പ്ലാറ്റ്ഫോം. സർട്ടിഫിക്കറ്റുകൾ, ഡോക്കുമെന്റുകൾ, സേവനങ്ങൾ ഓൺലൈനിൽ എളുപ്പത്തിൽ അപേക്ഷിക്കുക.",
            explore: "സേവനങ്ങൾ എക്സ്പ്ലോർ ചെയ്യുക",
            chat: "അസിസ്റ്റന്റുമായി ചാറ്റ് ചെയ്യുക"
        }
    };
    
    const t = translations[lang] || translations.en;
    
    // Update hero section
    const heroTitle = document.querySelector('.hero-title');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    const heroDescription = document.querySelector('.hero-description');
    const exploreBtn = document.getElementById('exploreServices');
    const chatBtn = document.getElementById('chatNow');
    
    if (heroTitle) heroTitle.innerHTML = heroTitle.innerHTML.replace(/Welcome to <span.*?>Agadh<\/span>/, `${t.welcome} <span class="highlight">Agadh</span>`);
    if (heroSubtitle) heroSubtitle.textContent = t.subtitle;
    if (heroDescription) heroDescription.textContent = t.description;
    if (exploreBtn) exploreBtn.innerHTML = `<i class="fas fa-search"></i> ${t.explore}`;
    if (chatBtn) chatBtn.innerHTML = `<i class="fas fa-comments"></i> ${t.chat}`;
}

// Scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Modal functions
function showLoginModal() {
    closeAllModals();
    document.getElementById('loginModal').classList.add('active');
}

function showRegisterModal() {
    closeAllModals();
    document.getElementById('registerModal').classList.add('active');
}

function showServiceModal(service) {
    closeAllModals();
    
    const modal = document.getElementById('serviceModal');
    const title = document.getElementById('serviceModalTitle');
    const body = document.getElementById('serviceModalBody');
    
    title.textContent = service.name;
    
    // Create modal content
    body.innerHTML = `
        <div class="service-modal-content">
            <div class="service-modal-header">
                <div class="service-icon-large">
                    <i class="fas ${service.icon || 'fa-cogs'}"></i>
                </div>
                <div class="service-info">
                    <h4>${service.department}</h4>
                    <p><i class="fas fa-clock"></i> Processing: ${service.processing_time}</p>
                    <p><i class="fas fa-rupee-sign"></i> Fee: ₹${service.fee}</p>
                </div>
            </div>
            
            <div class="service-modal-description">
                <h4>Description</h4>
                <p>${service.description}</p>
                ${service.detailed_description ? `<p>${service.detailed_description}</p>` : ''}
            </div>
            
            <div class="service-modal-documents">
                <h4><i class="fas fa-file-alt"></i> Required Documents</h4>
                <div class="documents-list" id="serviceDocumentsList">
                    <div class="loading">Loading documents...</div>
                </div>
            </div>
            
            <div class="service-modal-actions">
                <button class="btn btn-primary" onclick="applyForService('${service.slug}')">
                    <i class="fas fa-edit"></i> Apply Now
                </button>
                <button class="btn btn-outline" onclick="askAboutService('${service.name}')">
                    <i class="fas fa-question-circle"></i> Ask Assistant
                </button>
            </div>
        </div>
    `;
    
    modal.classList.add('active');
    
    // Load documents for this service
    loadServiceDocuments(service.slug);
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

// Load services from API
async function loadServices() {
    try {
        const response = await fetch('http://localhost:8000/api/services/');
        const data = await response.json();
        services = data.results || data;
        renderServices();
    } catch (error) {
        console.error('Error loading services:', error);
        // Load fallback data
        loadFallbackServices();
    }
}

function loadFallbackServices() {
    // Fallback services data
    services = [
        {
            id: 1,
            name: 'Ration Card Services',
            service_type: 'ration_card',
            description: 'Apply for new ration card, modifications, and transfers',
            icon: 'fa-id-card',
            fee: 50,
            processing_time: '7-10 working days',
            slug: 'ration-card',
            department: 'Civil Supplies Department'
        },
        {
            id: 2,
            name: 'Marriage Registration',
            service_type: 'marriage_registration',
            description: 'Register marriages and obtain marriage certificates',
            icon: 'fa-ring',
            fee: 100,
            processing_time: '3-5 working days',
            slug: 'marriage-registration',
            department: 'Local Administration'
        },
        {
            id: 3,
            name: 'Police Clearance Certificate',
            service_type: 'police_clearance',
            description: 'Obtain police clearance certificate for various purposes',
            icon: 'fa-shield-alt',
            fee: 500,
            processing_time: '10-15 working days',
            slug: 'police-clearance',
            department: 'Kerala Police'
        },
        {
            id: 4,
            name: 'PAN Card Services',
            service_type: 'pan_card',
            description: 'Apply for new PAN card, corrections, and updates',
            icon: 'fa-address-card',
            fee: 107,
            processing_time: '15-20 working days',
            slug: 'pan-card',
            department: 'Income Tax Department'
        },
        {
            id: 5,
            name: 'Birth Certificate Services',
            service_type: 'birth_certificate',
            description: 'Register births and obtain birth certificates',
            icon: 'fa-baby',
            fee: 30,
            processing_time: '3-7 working days',
            slug: 'birth-certificate',
            department: 'Local Self Government'
        },
        {
            id: 6,
            name: 'Passport Services',
            service_type: 'passport',
            description: 'Apply for new passport and related services',
            icon: 'fa-passport',
            fee: 1500,
            processing_time: '20-30 working days',
            slug: 'passport',
            department: 'Ministry of External Affairs'
        },
        {
            id: 7,
            name: 'Aadhaar Services',
            service_type: 'aadhaar',
            description: 'Aadhaar enrollment, updates, and corrections',
            icon: 'fa-fingerprint',
            fee: 0,
            processing_time: '15-20 working days',
            slug: 'aadhaar',
            department: 'UIDAI'
        },
        {
            id: 8,
            name: 'Death Registration Services',
            service_type: 'death_registration',
            description: 'Register deaths and obtain death certificates',
            icon: 'fa-cross',
            fee: 30,
            processing_time: '3-7 working days',
            slug: 'death-registration',
            department: 'Local Self Government'
        },
        {
            id: 9,
            name: 'Non-Creamy Layer Certificate',
            service_type: 'ncl_certificate',
            description: 'Apply for Non-Creamy Layer (OBC) certificate',
            icon: 'fa-certificate',
            fee: 100,
            processing_time: '10-15 working days',
            slug: 'ncl-certificate',
            department: 'Revenue Department'
        }
    ];
    
    renderServices();
}

function renderServices() {
    const servicesGrid = document.getElementById('servicesGrid');
    if (!servicesGrid) return;
    
    servicesGrid.innerHTML = '';
    
    services.forEach(service => {
        const serviceCard = document.createElement('div');
        serviceCard.className = 'service-card';
        serviceCard.onclick = () => showServiceModal(service);
        
        serviceCard.innerHTML = `
            <div class="service-icon">
                <i class="fas ${service.icon || 'fa-cogs'}"></i>
            </div>
            <div class="service-content">
                <h3 class="service-title">${service.name}</h3>
                <p class="service-description">${service.description}</p>
                <ul class="service-features">
                    <li><i class="fas fa-check-circle"></i> Processing: ${service.processing_time}</li>
                    <li><i class="fas fa-check-circle"></i> Fee: ₹${service.fee}</li>
                    <li><i class="fas fa-check-circle"></i> Department: ${service.department}</li>
                </ul>
                <div class="service-footer">
                    <span class="service-status">
                        <i class="fas fa-check text-success"></i> Available
                    </span>
                    <button class="btn btn-sm btn-primary">
                        View Details
                    </button>
                </div>
            </div>
        `;
        
        servicesGrid.appendChild(serviceCard);
    });
}

// Load employees from API
async function loadEmployees() {
    try {
        const response = await fetch('http://localhost:8000/api/employees/kozhikode/');
        const data = await response.json();
        employees = data;
        renderEmployees();
    } catch (error) {
        console.error('Error loading employees:', error);
        // Load fallback data
        loadFallbackEmployees();
    }
}

function loadFallbackEmployees() {
    // Fallback employees data (Kozhikode Akshaya Center)
    employees = [
        {
            id: 1,
            user: { first_name: 'Nandana', last_name: 'P P', get_full_name: 'Nandana P P' },
            employee_id: 'AKSH001',
            designation: 'Center Manager',
            department: 'Administration',
            official_phone: 'xxxxxxxxxx',
            rating: 4.8,
            experience_years: 8
        },
        {
            id: 2,
            user: { first_name: 'Abhishna', last_name: 'P P', get_full_name: 'Abhishna P P' },
            employee_id: 'AKSH002',
            designation: 'Computer Operator',
            department: 'Registration Services',
            official_phone: 'xxxxxxxxxx',
            rating: 4.6,
            experience_years: 5
        },
        {
            id: 3,
            user: { first_name: 'Theja', last_name: 'K', get_full_name: 'Theja K' },
            employee_id: 'AKSH003',
            designation: 'Assistant',
            department: 'Certificate Services',
            official_phone: 'xxxxxxxxxx',
            rating: 4.7,
            experience_years: 4
        },
        {
            id: 4,
            user: { first_name: 'Maya', last_name: 'S', get_full_name: 'Maya S' },
            employee_id: 'AKSH004',
            designation: 'Supervisor',
            department: 'Financial Services',
            official_phone: 'xxxxxxxxxx',
            rating: 4.9,
            experience_years: 6
        },
        {
            id: 5,
            user: { first_name: 'Vandana', last_name: 'T T K', get_full_name: 'Vandana T T K' },
            employee_id: 'AKSH005',
            designation: 'Coordinator',
            department: 'Customer Support',
            official_phone: 'xxxxxxxxxx',
            rating: 4.5,
            experience_years: 3
        }
    ];
    
    renderEmployees();
}

function renderEmployees() {
    const employeesGrid = document.getElementById('employeesGrid');
    if (!employeesGrid) return;
    
    employeesGrid.innerHTML = '';
    
    employees.forEach(employee => {
        const employeeCard = document.createElement('div');
        employeeCard.className = 'employee-card';
        
        employeeCard.innerHTML = `
            <div class="employee-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="employee-info">
                <h4 class="employee-name">${employee.user.get_full_name}</h4>
                <p class="employee-role">${employee.designation}</p>
                <p class="employee-department">${employee.department}</p>
                <p class="employee-contact">
                    <i class="fas fa-phone"></i> ${employee.official_phone}
                </p>
                <div class="employee-rating">
                    <i class="fas fa-star text-warning"></i>
                    <span>${employee.rating}</span>
                    <span class="text-muted">(${employee.experience_years} years exp.)</span>
                </div>
            </div>
        `;
        
        employeesGrid.appendChild(employeeCard);
    });
}

// Load service documents
async function loadServiceDocuments(serviceSlug) {
    const documentsList = document.getElementById('serviceDocumentsList');
    if (!documentsList) return;
    
    try {
        const response = await fetch(`http://localhost:8000/api/services/${serviceSlug}/documents/`);
        const serviceData = await response.json();
        
        if (serviceData.required_documents && serviceData.required_documents.length > 0) {
            let html = '<ul class="documents-items">';
            serviceData.required_documents.forEach(doc => {
                html += `
                    <li class="document-item">
                        <i class="fas ${doc.is_mandatory ? 'fa-file-exclamation text-danger' : 'fa-file text-info'}"></i>
                        <div>
                            <strong>${doc.name}</strong>
                            ${doc.description ? `<p class="text-muted">${doc.description}</p>` : ''}
                            <small class="text-muted">
                                ${doc.is_mandatory ? 'Mandatory' : 'Optional'} 
                                • Max size: ${doc.max_size_mb}MB
                            </small>
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            documentsList.innerHTML = html;
        } else {
            documentsList.innerHTML = '<p class="text-muted">No specific document requirements listed.</p>';
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        documentsList.innerHTML = `
            <p class="text-danger">
                <i class="fas fa-exclamation-triangle"></i>
                Could not load document requirements. Please try again.
            </p>
        `;
    }
}

// User authentication
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save tokens
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('user_data', JSON.stringify(data.user));
            
            currentUser = data.user;
            
            // Update UI
            updateUserUI();
            
            // Close modal
            closeAllModals();
            
            // Show success message
            showNotification('Login successful!', 'success');
        } else {
            showNotification(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Network error. Please try again.', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('registerUsername').value,
        email: document.getElementById('registerEmail').value,
        password: document.getElementById('registerPassword').value,
        confirm_password: document.getElementById('registerConfirmPassword').value,
        first_name: document.getElementById('registerFirstName').value,
        last_name: document.getElementById('registerLastName').value,
        phone: document.getElementById('registerPhone').value,
        preferred_language: document.getElementById('registerLanguage').value
    };
    
    // Basic validation
    if (formData.password !== formData.confirm_password) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:8000/api/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Auto login after registration
            const loginResponse = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: formData.username,
                    password: formData.password
                })
            });
            
            const loginData = await loginResponse.json();
            
            if (loginResponse.ok) {
                localStorage.setItem('access_token', loginData.access);
                localStorage.setItem('refresh_token', loginData.refresh);
                localStorage.setItem('user_data', JSON.stringify(loginData.user));
                
                currentUser = loginData.user;
                updateUserUI();
                closeAllModals();
                
                showNotification('Registration successful! Welcome to Agadh.', 'success');
            }
        } else {
            // Show validation errors
            let errorMsg = 'Registration failed: ';
            for (const field in data) {
                if (Array.isArray(data[field])) {
                    errorMsg += data[field].join(', ') + ' ';
                }
            }
            showNotification(errorMsg, 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('Network error. Please try again.', 'error');
    }
}

function checkUserSession() {
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user_data');
    
    if (token && userData) {
        try {
            currentUser = JSON.parse(userData);
            updateUserUI();
        } catch (e) {
            // Clear invalid data
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
        }
    }
}

function updateUserUI() {
    const userActions = document.querySelector('.user-actions');
    
    if (currentUser) {
        userActions.innerHTML = `
            <div class="user-dropdown">
                <button class="btn btn-outline" id="userMenu">
                    <i class="fas fa-user"></i> ${currentUser.first_name || currentUser.username}
                </button>
                <div class="dropdown-menu">
                    <a href="#profile" class="dropdown-item">
                        <i class="fas fa-user-circle"></i> Profile
                    </a>
                    <a href="#applications" class="dropdown-item">
                        <i class="fas fa-file-alt"></i> My Applications
                    </a>
                    <a href="#documents" class="dropdown-item">
                        <i class="fas fa-folder"></i> My Documents
                    </a>
                    <div class="dropdown-divider"></div>
                    <button class="dropdown-item" onclick="handleLogout()">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </button>
                </div>
            </div>
        `;
        
        // Add dropdown functionality
        const userMenu = document.getElementById('userMenu');
        if (userMenu) {
            userMenu.addEventListener('click', function(e) {
                e.stopPropagation();
                const dropdown = this.nextElementSibling;
                dropdown.classList.toggle('show');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function() {
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            });
        }
    } else {
        userActions.innerHTML = `
            <button class="btn btn-outline" id="loginBtn">
                <i class="fas fa-sign-in-alt"></i> Login
            </button>
            <button class="btn btn-primary" id="registerBtn">
                <i class="fas fa-user-plus"></i> Register
            </button>
        `;
        
        // Reattach event listeners
        document.getElementById('loginBtn').addEventListener('click', showLoginModal);
        document.getElementById('registerBtn').addEventListener('click', showRegisterModal);
    }
}

async function handleLogout() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    try {
        await fetch('http://localhost:8000/api/auth/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ refresh: refreshToken })
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    // Clear local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    
    currentUser = null;
    updateUserUI();
    
    showNotification('Logged out successfully', 'success');
}

// Chatbot functionality
function initChatbot() {
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotClose = document.getElementById('chatbotClose');
    const sendMessageBtn = document.getElementById('sendMessage');
    const chatInput = document.getElementById('chatInput');
    
    if (chatbotToggle) {
        chatbotToggle.addEventListener('click', toggleChatbot);
    }
    
    if (chatbotClose) {
        chatbotClose.addEventListener('click', toggleChatbot);
    }
    
    if (sendMessageBtn) {
        sendMessageBtn.addEventListener('click', sendChatMessage);
    }
    
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
}

function toggleChatbot() {
    const chatbot = document.getElementById('chatbotWidget');
    chatbot.classList.toggle('open');
}

async function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot';
    typingIndicator.innerHTML = `
        <div class="message-content">
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        // Send to Rasa directly
        const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sender: 'user_' + Date.now(),
                message: message
            })
        });
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (response.ok) {
            const data = await response.json();
            
            if (data && data.length > 0) {
                // Add bot response
                addChatMessage(data[0].text, 'bot');
            } else {
                addChatMessage('I can help you with government services. What service do you need assistance with?', 'bot');
            }
        } else {
            console.error('Rasa error:', response.status, await response.text());
            addChatMessage('I can help you with: Ration Card, Passport, Aadhaar, PAN Card, Marriage Registration, Police Clearance, Birth Certificate, Death Certificate, NCL Certificate. Which one are you interested in?', 'bot');
        }
    } catch (error) {
        console.error('Chatbot error:', error);
        typingIndicator.remove();
        addChatMessage('I\'m here to help! Try asking about document requirements for government services.', 'bot');
    }
}
function addChatMessage(text, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `
        <div class="message-content">${formatChatMessage(text)}</div>
        <div class="message-time">${getCurrentTime()}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatChatMessage(text) {
    // Convert line breaks and basic formatting
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\*(.*?)\*/g, '<i>$1</i>');
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addQuickAction(serviceType) {
    const chatMessages = document.getElementById('chatMessages');
    const quickAction = document.createElement('div');
    
    quickAction.className = 'quick-action';
    quickAction.innerHTML = `
        <div class="quick-action-content">
            <p>Would you like to:</p>
            <div class="quick-action-buttons">
                <button class="btn btn-sm btn-primary" onclick="showServiceByType('${serviceType}')">
                    View Service Details
                </button>
                <button class="btn btn-sm btn-outline" onclick="askAboutDocuments('${serviceType}')">
                    Ask About Documents
                </button>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(quickAction);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Service actions
function applyForService(serviceSlug) {
    if (!currentUser) {
        showNotification('Please login to apply for services', 'warning');
        showLoginModal();
        return;
    }
    
    // In a real app, this would navigate to application form
    showNotification(`Application for ${serviceSlug} would start here`, 'info');
    closeAllModals();
}

function askAboutService(serviceName) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = `Tell me about ${serviceName}`;
    
    closeAllModals();
    toggleChatbot();
    
    // Auto send after a delay
    setTimeout(() => {
        sendChatMessage();
    }, 500);
}

function askAboutDocuments(serviceType) {
    const serviceNames = {
        'ration_card': 'ration card',
        'marriage_registration': 'marriage registration',
        'police_clearance': 'police clearance certificate',
        'pan_card': 'PAN card',
        'birth_certificate': 'birth certificate',
        'passport': 'passport',
        'aadhaar': 'Aadhaar',
        'death_registration': 'death registration',
        'ncl_certificate': 'non-creamy layer certificate'
    };
    
    const serviceName = serviceNames[serviceType] || serviceType;
    const chatInput = document.getElementById('chatInput');
    chatInput.value = `What documents are required for ${serviceName}?`;
    
    toggleChatbot();
    setTimeout(() => {
        sendChatMessage();
    }, 500);
}

function showServiceByType(serviceType) {
    const service = services.find(s => s.service_type === serviceType);
    if (service) {
        showServiceModal(service);
    } else {
        showNotification('Service not found', 'error');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
    
    // Add styles if not already present
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                min-width: 300px;
                max-width: 400px;
                z-index: 2000;
                animation: slideIn 0.3s ease;
                color: white;
            }
            
            .notification-info { background-color: #17a2b8; }
            .notification-success { background-color: #28a745; }
            .notification-warning { background-color: #ffc107; color: #212529; }
            .notification-error { background-color: #dc3545; }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                flex: 1;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: inherit;
                cursor: pointer;
                margin-left: 1rem;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }
}

function getNotificationIcon(type) {
    const icons = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-exclamation-circle'
    };
    return icons[type] || icons.info;
}

// Utility function to get auth headers
function getAuthHeaders() {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
}

// Initialize with saved language
const savedLanguage = localStorage.getItem('agadh_language') || 'en';
setLanguage(savedLanguage);