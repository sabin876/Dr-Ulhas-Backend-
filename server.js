const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const apiRoutes = require('./routes/api');
const AdminJS = require('adminjs');
const AdminJSExpress = require('@adminjs/express');
const AdminJSSequelize = require('@adminjs/sequelize');
const { sequelize, Article, Service, Translation, SiteSetting } = require('./models');
const session = require('express-session');

AdminJS.registerAdapter(AdminJSSequelize);

const app = express();
const PORT = process.env.PORT || 5000;

// AdminJS setup
const adminJs = new AdminJS({
    resources: [
        { resource: Article, options: { parent: { name: 'Content' } } },
        { resource: Service, options: { parent: { name: 'Content' } } },
        { resource: Translation, options: { parent: { name: 'Localization' } } },
        { resource: SiteSetting, options: { parent: { name: 'Settings' } } },
    ],
    rootPath: '/admin',
    branding: {
        companyName: 'Dr. Ulhas Sonar',
        logo: false,
    }
});

const adminRouter = AdminJSExpress.buildRouter(adminJs);

// Middleware
app.use(helmet({
    contentSecurityPolicy: false,
}));
app.use(cors({
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true
}));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Session for AdminJS
app.use(session({
    secret: process.env.SESSION_SECRET || 'secret-key-dr-ulhas',
    resave: false,
    saveUninitialized: true,
}));

// Routes
app.use(adminJs.options.rootPath, adminRouter);
app.use('/api', apiRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
