import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSelectModule } from '@angular/material/select';
import { UserResponse, OrganizationResponse, RoleBase } from '../../services/api';
import { ApiService } from '../../services/api';

@Component({
    selector: 'app-user-dialog',
    template: `
    <h2 mat-dialog-title>{{ data ? 'Edit User' : 'Add User' }}</h2>
    <mat-dialog-content>
      <form [formGroup]="userForm" class="user-form">
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>First Name</mat-label>
          <input matInput formControlName="first_name" required>
          <mat-error *ngIf="userForm.get('first_name')?.hasError('required')">
            First name is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Last Name</mat-label>
          <input matInput formControlName="last_name" required>
          <mat-error *ngIf="userForm.get('last_name')?.hasError('required')">
            Last name is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Email</mat-label>
          <input matInput type="email" formControlName="email" required>
          <mat-error *ngIf="userForm.get('email')?.hasError('required')">
            Email is required
          </mat-error>
          <mat-error *ngIf="userForm.get('email')?.hasError('email')">
            Please enter a valid email
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Role</mat-label>
          <mat-select formControlName="role">
            <mat-option *ngFor="let role of roles" [value]="role.name">
              {{ role.name }}
            </mat-option>
          </mat-select>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Organization</mat-label>
          <mat-select formControlName="organization">
            <mat-option value="">None</mat-option>
            <mat-option *ngFor="let org of organizations" [value]="org.name">
              {{ org.name }}
            </mat-option>
          </mat-select>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width" *ngIf="!data">
          <mat-label>Password</mat-label>
          <input matInput type="password" formControlName="password" [required]="!data">
          <mat-error *ngIf="userForm.get('password')?.hasError('required')">
            Password is required for new users
          </mat-error>
        </mat-form-field>
      </form>
    </mat-dialog-content>
    
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-raised-button color="primary" 
              (click)="onSave()" 
              [disabled]="!userForm.valid">
        {{ data ? 'Update' : 'Create' }}
      </button>
    </mat-dialog-actions>
  `,
    styles: [`
    .user-form {
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 400px;
    }
    
    .full-width {
      width: 100%;
    }
  `],
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        MatDialogModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatSelectModule
    ]
})
export class UserDialog {
    userForm: FormGroup;
    organizations: OrganizationResponse[] = [];
    roles: RoleBase[] = [];

    constructor(
        private fb: FormBuilder,
        private dialogRef: MatDialogRef<UserDialog>,
        @Inject(MAT_DIALOG_DATA) public data: UserResponse | null,
        private apiService: ApiService
    ) {
        this.userForm = this.fb.group({
            first_name: [data?.first_name || '', [Validators.required]],
            last_name: [data?.last_name || '', [Validators.required]],
            email: [data?.email || '', [Validators.required, Validators.email]],
            role: [data?.role || ''],
            organization: [data?.organization || ''],
            password: [!data ? '' : null, !data ? [Validators.required] : []]
        });

        this.loadOrganizations();
        this.loadRoles();
    }

    loadOrganizations() {
        this.apiService.getOrganizations().subscribe({
            next: (orgs) => this.organizations = orgs,
            error: (error) => console.error('Error loading organizations:', error)
        });
    }

    loadRoles() {
        this.apiService.getRoles().subscribe({
            next: (roles) => this.roles = roles,
            error: (error) => console.error('Error loading roles:', error)
        });
    }

    onCancel(): void {
        this.dialogRef.close();
    }

    onSave(): void {
        if (this.userForm.valid) {
            const userData = {
                ...this.userForm.value,
                ...(this.data?.id && { id: this.data.id })
            };
            if (this.data && userData.password === null) {
                delete userData.password;
            }
            this.dialogRef.close(userData);
        }
    }
}
