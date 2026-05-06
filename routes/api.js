const express = require('express');
const router = express.Router();
const apiController = require('../controllers/apiController');

router.get('/articles', apiController.getArticles);
router.get('/articles/:slug', apiController.getArticleBySlug);
router.get('/services', apiController.getServices);
router.get('/translations', apiController.getTranslations);
router.get('/settings', apiController.getSiteSettings);

module.exports = router;
