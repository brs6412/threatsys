import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Users } from './components/users/users';
import { Iocs } from './components/iocs/iocs';
import { PageNotFound } from './components/page-not-found/page-not-found';

export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: Home },
    { path: 'users', component: Users },
    { path: 'iocs', component: Iocs },
    { path: '**', component: PageNotFound }
];