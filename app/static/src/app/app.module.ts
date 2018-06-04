import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

// Boostrap
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

// Material
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSidenavModule } from '@angular/material/sidenav';
import { LayoutModule } from '@angular/cdk/layout';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatInputModule } from '@angular/material';
import { MatIconRegistry } from '@angular/material';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatButtonModule } from '@angular/material/button';

// Dependencies
import { RouterModule, Routes } from '@angular/router';

// Componnents
import { AppComponent } from './app.component';
import { InAppComponent } from './in-app/in-app.component';
import { OutAppComponent } from './out-app/out-app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LogInComponent } from './log-in/log-in.component';

@NgModule({
  declarations: [
    AppComponent,
    AppComponent,
    InAppComponent,
    OutAppComponent,
    DashboardComponent,
    LogInComponent
  ],
  imports     : [
    BrowserModule,
    MDBBootstrapModule.forRoot(),
    BrowserAnimationsModule,
    AppRoutingModule,
    MatSidenavModule,
    LayoutModule,
    MatListModule,
    MatIconModule,
    MatToolbarModule,
    ReactiveFormsModule,
    FormsModule,
    MatFormFieldModule,
    MatCheckboxModule,
    MatInputModule,
    MatCardModule,
    MatTabsModule,
    MatButtonModule
  ],
  schemas     : [NO_ERRORS_SCHEMA],
  providers   : [
    MatIconRegistry
  ],
  bootstrap   : [AppComponent]
})
export class AppModule { }
