import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Componnents
import { AppComponent } from './app.component';
import { InAppComponent } from './in-app/in-app.component';
import { OutAppComponent } from './out-app/out-app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LogInComponent } from './log-in/log-in.component';


export const routes: Routes = [
  {
    path: 'outApp',
    component: OutAppComponent,
    children: [
        { path: '', redirectTo: 'logIn', pathMatch: 'full' },
        { path: 'logIn', component: LogInComponent },
        { path: '**', component: LogInComponent }
    ]
  },
  {
    path: '',
    component: InAppComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent},
      { path: '**', component: DashboardComponent}
    ]
  },
  {
    path: '**', redirectTo: 'dashboard'
  }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
