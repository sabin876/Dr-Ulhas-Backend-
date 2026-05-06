import express from 'express';
const router = express.Router();
import * as apiController from '../controllers/apiController.js';

router.get('/articles', apiController.getArticles);
router.get('/articles/:slug', apiController.getArticleBySlug);
router.get('/services', apiController.getServices);
router.get('/translations', apiController.getTranslations);
router.get('/settings', apiController.getSiteSettings);

export default router;
