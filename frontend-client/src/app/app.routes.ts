import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Iocs } from './components/iocs/iocs';
import { Users } from './components/users/users';
import { PageNotFound } from './components/page-not-found/page-not-found';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'iocs', component: Iocs },
    { path: 'users', component: Users },
    { path: '**', component: PageNotFound }
];
