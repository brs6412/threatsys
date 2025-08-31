import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatChipsModule } from '@angular/material/chips';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService, IOCResponse, IOCDetailResponse, IOCCreate, IOCUpdate, IOCTypeResponse } from '../../services/api';
import { IocDialog } from './ioc-dialog';

@Component({
  selector: 'app-iocs',
  templateUrl: './iocs.html',
  styleUrls: ['./iocs.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatChipsModule,
    MatSnackBarModule,
    MatProgressSpinnerModule
  ]
})
export class Iocs implements OnInit {
  iocs: IOCResponse[] = [];
  displayedColumns: string[] = ['id', 'value', 'ioc_type', 'tlp_level', 'active', 'source_organization', 'last_seen', 'actions'];
  loading = false;

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.loadIOCs();
  }

  loadIOCs() {
    this.loading = true;
    this.apiService.getIOCs().subscribe({
      next: (iocs) => {
        this.iocs = iocs;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading IOCs:', error);
        this.snackBar.open('Error loading IOCs', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  openIocDialog(ioc?: IOCResponse) {
    const dialogRef = this.dialog.open(IocDialog, {
      width: '600px',
      data: ioc || null
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (result.id) {
          this.updateIOC(result.id, result);
        } else {
          this.createIOC(result);
        }
      }
    });
  }

  createIOC(ioc: IOCCreate) {
    this.apiService.createIOC(ioc).subscribe({
      next: (newIOC) => {
        this.iocs.push(newIOC);
        this.snackBar.open('IOC created successfully', 'Close', { duration: 3000 });
      },
      error: (error) => {
        console.error('Error creating IOC:', error);
        this.snackBar.open('Error creating IOC', 'Close', { duration: 3000 });
      }
    });
  }

  updateIOC(id: string, ioc: IOCUpdate) {
    this.apiService.updateIOC(id, ioc).subscribe({
      next: (updatedIOC) => {
        const index = this.iocs.findIndex(i => i.id === id);
        if (index !== -1) {
          this.iocs[index] = updatedIOC;
        }
        this.snackBar.open('IOC updated successfully', 'Close', { duration: 3000 });
      },
      error: (error) => {
        console.error('Error updating IOC:', error);
        this.snackBar.open('Error updating IOC', 'Close', { duration: 3000 });
      }
    });
  }

  deleteIOC(id: string) {
    if (confirm('Are you sure you want to delete this IOC?')) {
      this.apiService.deleteIOC(id).subscribe({
        next: () => {
          this.iocs = this.iocs.filter(i => i.id !== id);
          this.snackBar.open('IOC deleted successfully', 'Close', { duration: 3000 });
        },
        error: (error) => {
          console.error('Error deleting IOC:', error);
          this.snackBar.open('Error deleting IOC', 'Close', { duration: 3000 });
        }
      });
    }
  }

  getTLPColor(tlpLevel: string): string {
    switch (tlpLevel.toLowerCase()) {
      case 'red': return 'warn';
      case 'amber': return 'accent';
      case 'green': return 'primary';
      case 'white': return '';
      default: return '';
    }
  }
}