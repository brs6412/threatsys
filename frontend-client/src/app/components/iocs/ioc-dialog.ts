import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { IOCResponse, IOCCreate, IOCUpdate, IOCTypeResponse } from '../../services/api';
import { ApiService } from '../../services/api';

@Component({
    selector: 'app-ioc-dialog',
    template: `
    <h2 mat-dialog-title>{{ data ? 'Edit IOC' : 'Add IOC' }}</h2>
    <mat-dialog-content>
      <form [formGroup]="iocForm" class="ioc-form">
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>IOC Value</mat-label>
          <input matInput formControlName="value" required
                 placeholder="e.g., 192.168.1.1, malware.exe, evil.com">
          <mat-error *ngIf="iocForm.get('value')?.hasError('required')">
            IOC value is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>IOC Type</mat-label>
          <mat-select formControlName="ioc_type_id" required>
            <mat-option *ngFor="let type of iocTypes" [value]="type.id">
              {{ type.name }}
              <span *ngIf="type.category"> ({{ type.category }})</span>
            </mat-option>
          </mat-select>
          <mat-error *ngIf="iocForm.get('ioc_type_id')?.hasError('required')">
            IOC type is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>TLP Level</mat-label>
          <mat-select formControlName="tlp_level" required>
            <mat-option value="white">TLP:WHITE</mat-option>
            <mat-option value="green">TLP:GREEN</mat-option>
            <mat-option value="amber">TLP:AMBER</mat-option>
            <mat-option value="red">TLP:RED</mat-option>
          </mat-select>
          <mat-error *ngIf="iocForm.get('tlp_level')?.hasError('required')">
            TLP level is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Source Organization</mat-label>
          <input matInput formControlName="source_organization"
                 placeholder="Optional source organization">
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Creator</mat-label>
          <input matInput formControlName="creator"
                 placeholder="Optional creator information">
        </mat-form-field>

        <mat-checkbox formControlName="active" class="full-width">
          Active IOC
        </mat-checkbox>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Metadata (JSON)</mat-label>
          <textarea matInput formControlName="metadata_json" rows="3"
                    placeholder='Optional metadata as JSON, e.g., {"confidence": "high"}'></textarea>
          <mat-error *ngIf="iocForm.get('metadata_json')?.hasError('invalidJson')">
            Please enter valid JSON
          </mat-error>
        </mat-form-field>
      </form>
    </mat-dialog-content>
    
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-raised-button color="primary" 
              (click)="onSave()" 
              [disabled]="!iocForm.valid">
        {{ data ? 'Update' : 'Create' }}
      </button>
    </mat-dialog-actions>
  `,
    styles: [`
    .ioc-form {
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 500px;
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
        MatSelectModule,
        MatCheckboxModule
    ]
})
export class IocDialog {
    iocForm: FormGroup;
    iocTypes: IOCTypeResponse[] = [];

    constructor(
        private fb: FormBuilder,
        private dialogRef: MatDialogRef<IocDialog>,
        @Inject(MAT_DIALOG_DATA) public data: IOCResponse | null,
        private apiService: ApiService
    ) {
        this.iocForm = this.fb.group({
            value: [data?.value || '', [Validators.required]],
            ioc_type_id: [data?.ioc_type.id || '', [Validators.required]],
            tlp_level: [data?.tlp_level || 'white', [Validators.required]],
            source_organization: [data?.source_organization || ''],
            creator: [data?.creator || ''],
            active: [data?.active !== undefined ? data.active : true],
            metadata_json: ['', this.jsonValidator]
        });

        // Load IOC types
        this.loadIOCTypes();

        // If editing, populate metadata as JSON string
        if (data && (data as any).metadata_) {
            this.iocForm.patchValue({
                metadata_json: JSON.stringify((data as any).metadata_, null, 2)
            });
        }
    }

    loadIOCTypes() {
        this.apiService.getIOCTypes().subscribe({
            next: (types) => this.iocTypes = types,
            error: (error) => console.error('Error loading IOC types:', error)
        });
    }

    jsonValidator(control: any) {
        if (!control.value) return null; // Empty is valid
        try {
            JSON.parse(control.value);
            return null;
        } catch {
            return { invalidJson: true };
        }
    }

    onCancel(): void {
        this.dialogRef.close();
    }

    onSave(): void {
        if (this.iocForm.valid) {
            const formData = { ...this.iocForm.value };

            // Parse JSON metadata if provided
            if (formData.metadata_json) {
                try {
                    formData.metadata_ = JSON.parse(formData.metadata_json);
                } catch {
                    // Should not happen due to validator, but just in case
                    delete formData.metadata_;
                }
            }
            delete formData.metadata_json;

            const iocData = {
                ...formData,
                ...(this.data?.id && { id: this.data.id })
            };

            this.dialogRef.close(iocData);
        }
    }
}