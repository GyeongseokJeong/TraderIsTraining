import { Outlet } from 'react-router-dom';
import { WarningBanner } from '../../shared/ui/WarningBanner';

export function AppLayout() { return <><WarningBanner /><Outlet /></>; }
