const { Sequelize, DataTypes } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
    host: process.env.DB_HOST,
    dialect: 'mysql',
    logging: false
});

const Article = sequelize.define('Article', {
    meta_title: { type: DataTypes.STRING },
    meta_description: { type: DataTypes.TEXT },
    canonical_url: { type: DataTypes.STRING },
    og_title: { type: DataTypes.STRING },
    og_description: { type: DataTypes.TEXT },
    og_image: { type: DataTypes.STRING },
    schema_markup: { type: DataTypes.JSON },
    index_page: { type: DataTypes.BOOLEAN, defaultValue: true },
    follow_links: { type: DataTypes.BOOLEAN, defaultValue: true },
    image_alt_text: { type: DataTypes.STRING },
    h1_title: { type: DataTypes.STRING },
    title: { type: DataTypes.STRING, allowNull: false },
    slug: { type: DataTypes.STRING, unique: true },
    excerpt: { type: DataTypes.TEXT },
    content: { type: DataTypes.TEXT },
    image: { type: DataTypes.STRING },
    author: { type: DataTypes.STRING, defaultValue: 'Dr. Ulhas Sonar' },
    category: { type: DataTypes.STRING },
    category_color: { type: DataTypes.STRING, defaultValue: 'bg-blue-100 text-blue-600' },
    date: { type: DataTypes.DATEONLY, defaultValue: Sequelize.NOW },
}, {
    tableName: 'api_article',
    timestamps: true,
    updatedAt: 'updated_at',
    createdAt: false
});

const Service = sequelize.define('Service', {
    meta_title: { type: DataTypes.STRING },
    meta_description: { type: DataTypes.TEXT },
    canonical_url: { type: DataTypes.STRING },
    og_title: { type: DataTypes.STRING },
    og_description: { type: DataTypes.TEXT },
    og_image: { type: DataTypes.STRING },
    schema_markup: { type: DataTypes.JSON },
    index_page: { type: DataTypes.BOOLEAN, defaultValue: true },
    follow_links: { type: DataTypes.BOOLEAN, defaultValue: true },
    image_alt_text: { type: DataTypes.STRING },
    h1_title: { type: DataTypes.STRING },
    title: { type: DataTypes.STRING, allowNull: false },
    slug: { type: DataTypes.STRING, unique: true },
    description: { type: DataTypes.TEXT },
    icon: { type: DataTypes.STRING },
    image: { type: DataTypes.STRING },
    items: { type: DataTypes.JSON },
}, {
    tableName: 'api_service',
    timestamps: true,
    updatedAt: 'updated_at',
    createdAt: false
});

const Translation = sequelize.define('Translation', {
    key: { type: DataTypes.STRING, allowNull: false },
    language: { type: DataTypes.STRING, allowNull: false },
    value: { type: DataTypes.JSON, allowNull: false },
}, {
    tableName: 'api_translation',
    timestamps: false
});

const SiteSetting = sequelize.define('SiteSetting', {
    robots_txt: { type: DataTypes.TEXT },
    header_scripts: { type: DataTypes.TEXT },
    footer_scripts: { type: DataTypes.TEXT },
    internal_linking_rules: { type: DataTypes.JSON },
}, {
    tableName: 'api_sitesetting',
    timestamps: false
});

module.exports = {
    sequelize,
    Article,
    Service,
    Translation,
    SiteSetting
};
