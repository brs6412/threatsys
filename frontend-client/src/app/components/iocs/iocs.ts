import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Api, IOC } from '../../services/api';

@Component({
  selector: 'app-iocs',
  imports: [CommonModule],
  templateUrl: './iocs.html',
  styleUrl: './iocs.scss'
})
export class Iocs {
  iocs: IOC[] = [];
  loading = true;
  error = '';

  constructor(private apiService: Api) { }

  ngOnInit(): void {
    this.apiService.getIocs().subscribe({
      next: (data) => {
        this.iocs = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load IOCs';
        console.error(err);
        this.loading = false;
      }
    });
  }
}
