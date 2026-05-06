import { Article, Service, Translation, SiteSetting } from '../models/index.js';

export const getArticles = async (req, res) => {
    try {
        const articles = await Article.findAll({ order: [['date', 'DESC']] });
        res.json(articles);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const getArticleBySlug = async (req, res) => {
    try {
        const article = await Article.findOne({ where: { slug: req.params.slug } });
        if (!article) return res.status(404).json({ error: 'Article not found' });
        res.json(article);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const getServices = async (req, res) => {
    try {
        const services = await Service.findAll();
        res.json(services);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const getTranslations = async (req, res) => {
    try {
        const language = (req.query.lang || 'EN').toUpperCase();
        const translationsList = await Translation.findAll({ where: { language } });
        
        const translations = {};
        translationsList.forEach(t => {
            translations[t.key] = t.value;
        });
        
        res.json(translations);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

export const getSiteSettings = async (req, res) => {
    try {
        const settings = await SiteSetting.findOne();
        res.json(settings || {});
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
