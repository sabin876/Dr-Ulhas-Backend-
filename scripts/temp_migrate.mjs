import { translations } from './dr-ulhas-ortho/src/translations.js';
import { articles } from './dr-ulhas-ortho/src/constants/articlesData.js';
import fs from 'fs';

const data = { translations, articles };
fs.writeFileSync('./dr-ulhas-backend/data_dump.json', JSON.stringify(data, null, 2));
console.log('Data dumped to dr-ulhas-backend/data_dump.json');
